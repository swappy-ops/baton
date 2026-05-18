import ollama
import chromadb
from sentence_transformers import SentenceTransformer

# Connect to PC-hosted Ollama
client = ollama.Client(
    host='http://192.168.1.19:11434'
)

# Embedding model
embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Persistent memory storage
db = chromadb.PersistentClient(
    path="./baton_memory"
)

# Load collection if it exists
try:
    collection = db.get_collection(
        "baton"
    )
except:
    collection = db.create_collection(
        "baton"
    )


while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("\nSaving memory...")
        break

    # Create embedding
    embedding = embed_model.encode(
        user_input
    ).tolist()

    # Store memory
    memory_id = str(
        collection.count()
    )

    collection.add(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[
            f"User stated: {user_input}"
        ]
    )

    # Retrieve related memories
    memories = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    context = "\n".join(
        memories["documents"][0]
    )

    # Generate response
    response = client.chat(
        model='qwen2.5-coder:7b',
        messages=[
            {
                "role": "system",
                "content": """
You are Baton.

Rules:
- Treat retrieved memories as facts.
- Use memory naturally.
- Mention relevant memories when useful.
- Do not invent facts.
- Prioritize recalled information.
"""
            },
            {
                "role": "user",
                "content": f"""
Retrieved Memory:

{context}

Current User Input:

{user_input}
"""
            }
        ]
    )

    print(
        "\nBaton:",
        response["message"]["content"]
    )
