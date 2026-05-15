# RETRIEVAL_RULES.md - Governance of Semantic Recall

## 1. Retrieval Gating
- All specialist nodes MUST invoke the `Neural Observatory` before execution.
- Retrieval query must be synthesized from the current task and history.

## 2. Payload Constraints
- Max context injection: 2000 tokens.
- Relevance floor: 0.7 cosine similarity.

## 3. Prioritization
1. Explicitly requested files.
2. Canonical DOS documentation (Rules/Constraints).
3. Distilled semantic artifacts from prior sessions.

## 4. Bias Control
- Prioritize architectural continuity over speculative generative patterns.
- Reject retrieval results that conflict with `GLOBAL_RULES.md`.
