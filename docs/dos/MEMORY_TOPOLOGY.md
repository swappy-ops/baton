# MEMORY_TOPOLOGY.md - Spatial Data Architecture

## 1. Hierarchy of Recall
1. **L1: Active State** (LangGraph `messages`) - High fidelity, low duration.
2. **L2: Distilled Artifacts** (`memory/distilled/*.md`) - Structured, mid-range duration.
3. **L3: Neural Observatory** (`embeddings/chroma`) - Semantic, long-term persistence.

## 2. Storage Schema
- **Path**: `memory/distilled/`
- **Format**: Markdown with YAML frontmatter.
- **Index**: ChromaDB `projskep_docs` collection.

## 3. Data Flow
- `DistillationNode` -> `MemoryManager` -> `ChromaDB`
- `RetrievalPipeline` -> `Neural Observatory` -> `SpecialistNode`
