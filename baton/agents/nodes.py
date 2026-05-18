from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from baton.retrieval.pipeline import get_retrieval_pipeline
from baton.runtime.task_contract import get_contract_for_task
from baton.runtime.context_budget import get_context_budget_manager
from baton.runtime.stability import get_stability_manager

budget_manager = get_context_budget_manager()
stability_manager = get_stability_manager()

def get_model(model_name: str):
    return ChatOllama(model=model_name, temperature=0)

def intent_router_node(state):
    print("--- ROUTING ---")
    messages = state["messages"]
    last_message = messages[-1].content
    
    # Use phi4 for routing
    model = get_model("phi4")
    prompt = f"Classify the following user request: 'code', 'ux', or 'music'. Return ONLY the word.\n\nRequest: {last_message}"
    response = model.invoke([HumanMessage(content=prompt)])
    task_type = response.content.strip().lower()
    
    if task_type not in ["code", "ux", "music"]:
        task_type = "code"
        
    contract = get_contract_for_task(task_type)
    return {
        "task_type": task_type,
        "contract": contract.__dict__
    }

def retrieval_node(state):
    print("--- NEURAL OBSERVATORY: RETRIEVING ---")
    query = state["messages"][-1].content
    task_type = state["task_type"]
    
    # Phase 4: Dynamic Budgeting
    budget = budget_manager.get_budget(task_type, "phi4") # Assume phi4 for retrieval logic
    limit = budget["retrieval_limit"]
    
    pipeline = get_retrieval_pipeline()
    
    if task_type == "music":
        # Specific filter or logic for music docs
        print("Music context requested - prioritized plugin chains and production notes.")
        results = pipeline.query(f"Music production: {query}", n_results=limit)
    else:
        results = pipeline.query(query, n_results=limit)
        
    context = "\n".join(results['documents'][0]) if results['documents'] else "No relevant context found in Neural Observatory."
    
    # Phase 7: Context Overflow Protection
    if stability_manager.handle_context_overflow(len(context.split()), budget["max_tokens"]):
        context = " ".join(context.split()[:budget["max_tokens"]]) # Hard truncate for safety
        
    return {"context": context}

def specialist_node(state):
    task_type = state["task_type"]
    contract = state["contract"]
    context = state["context"]
    messages = state["messages"]
    
    # Phase 4/7: Stability & Budget Awareness
    budget = budget_manager.get_budget(task_type, contract["model_name"])
    stability_manager.monitor_vram()
    
    print(f"--- COGNITION SPECIALIST: {task_type} ({contract['model_name']}) ---")
    
    model = get_model(contract["model_name"])
    
    system_msg = f"You are a Baton {task_type} specialist operating within the Forensic Industrial Interface.\nBounded Tools: {contract['allowed_tools']}\nNeural Observatory Context: {context}\nGuidelines: Retrieval-first, deterministic, semantic continuity preservation."
    
    try:
        response = model.invoke([AIMessage(content=system_msg)] + messages)
    except Exception as e:
        stability_manager.recovery_protocol("SpecialistNode")
        response = AIMessage(content=f"Error during specialized cognition: {e}. Degrading gracefully.")
        
    return {"messages": [response]}

from baton.agents.distillation_node import distillation_node
