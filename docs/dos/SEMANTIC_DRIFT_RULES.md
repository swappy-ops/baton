# SEMANTIC_DRIFT_RULES.md - Continuity Guardrails

## 1. Definition of Drift
Semantic drift occurs when the system begins using non-canonical terminology or deviates from established architectural patterns.

## 2. Detection Triggers
- Use of "dashboard" instead of "instrument".
- Use of "vector database" instead of "Neural Observatory".
- Introduction of SaaS-style generic UX patterns.

## 3. Correction Protocol
1. **Detection**: `dos_sync.py` identifies non-canonical token usage.
2. **Logging**: Record the drift event in `traces/validation/`.
3. **Normalization**: Force-replace terms in the current context.
4. **Reinforcement**: Inject `TERMINOLOGY.md` into the next retrieval cycle.

## 4. Pruning
- Prune redundant or conflicting memory entries that contribute to drift.
