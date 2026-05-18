# SEMANTIC_CONTINUITY.md - Memory Constitutional Layer

## 1. Continuity Rules
- **Terminology Enforcement**: All outputs must be normalized against `TERMINOLOGY.md`.
- **Bounded Retrieval**: Retrieval payloads injected into specialist contexts must remain under 2k tokens.
- **Forensic Precision**: Every memory entry must reference its source task and specialist.

## 2. Memory Boundaries
- **Working Memory**: Transient, runtime-only state (LangGraph state).
- **Distilled Memory**: Markdown-based artifacts for long-term reference.
- **Semantic Vector Memory**: Chroma-backed indices for efficient recall.

## 3. Retrieval Governance
- **Injection Priority**: Specialist context > Relevant distilled artifacts > Global rules.
- **Retrieval Thresholds**: Relevance score must meet the 0.7 floor for auto-injection.

## 4. Distillation Lifecycle
1. **Extraction**: Identify architectural patterns and decisions.
2. **Normalization**: Align with canonical Baton DOS language.
3. **Compression**: Reduce history to high-density semantic markers.
4. **Indexing**: Embed into the Neural Observatory.

## 5. Pruning & Aging
- **Redundancy Pruning**: Deduplicate entries with >85% semantic overlap.
- **Aging Policy**: Low-frequency reuse memories are archived after 30 cycles.
- **Drift Handling**: Semantic drift detections trigger a normalization pass.
