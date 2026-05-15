# NODE_RESPONSIBILITIES.md - Logic Layer Contracts

## 1. Intent Router (phi4)
- **Responsibility**: Classify incoming requests into Code, UX, or Music domains.
- **Output**: Task contract assignment.

## 2. Retrieval Node (Neural Observatory)
- **Responsibility**: Query the vector index and inject semantic context.
- **Constraint**: Maintain <2k token payload.

## 3. Specialist Nodes (qwen2.5-coder / phi4)
- **Responsibility**: Execute domain-specific logic.
- **Constraint**: Retrieval-first, deterministic execution.

## 4. Distillation Node
- **Responsibility**: Compress history into reusable semantic artifacts.
- **Output**: Markdown summaries and Chroma embeddings.

## 5. DOS Sync Engine
- **Responsibility**: Validate terminology and enforce canonical consistency.
