# GLOBAL_RULES.md - ProjSkep DOS Runtime Specification

## Core Directives
1. **Semantic Continuity**: All terminology must align with `TERMINOLOGY.md`.
2. **Implementation Realism**: Prioritize bounded execution and local hardware efficiency (Ryzen 5 / RX 6600).
3. **Retrieval-First**: All specialist nodes must be gated by semantic retrieval.
4. **Cinematic UX**: Interfaces must feel like forensic instruments, not SaaS dashboards.

## Architecture Constraints
- Strict separation between UI (WebView2), DSP, and Cognition.
- Use `@SafeThread` for background-to-UI interactions.
- Prevent DOM thrashing and blocking the message thread.

## AI Behavior
- Collaborator role, not autonomous director.
- Conservative inference; avoid recursive hallucination.
