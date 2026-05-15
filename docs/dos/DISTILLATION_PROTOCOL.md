# DISTILLATION_PROTOCOL.md - Cognitive Compression Standards

## 1. Objective
Transform verbose execution history into high-density architectural markers to prevent memory bloat and context exhaustion.

## 2. Extraction Criteria
- **Decisions**: Why a specific architectural path was chosen.
- **Constraints**: Hardware or software limitations discovered.
- **Patterns**: Reusable logic or UI structures.
- **Term Drift**: Instances where non-canonical language was used.

## 3. Compression Ratios
- Target: 10:1 (1000 lines of history -> 100 lines of distillation).
- Limit: Maximum 500 words per artifact.

## 4. Terminology Normalization
- Mandatory pass using `runtime/dos_sync.py` rules.
- Replace generic terms with ProjSkep canonical equivalents.
