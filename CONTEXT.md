## Baton — Current State (May 2026)
### Verified working
- Docker: docker run --rm -d --name baton-prod -p 8000:8000 -v $(pwd):/app baton:latest
- API: http://localhost:8000/api/status → operational
- UI: http://localhost:8000 → observatory, real telemetry, no simulated drift
- WS: keepalive fixed, holds indefinitely
- baton_server/* — coherent, DO NOT TOUCH
- baton/* — real package, imports resolve
- Legacy cleanup complete — zero projskep references remain in active code
- MIT LICENSE added
- GitHub Actions audit workflow added
- Canonical repo structure in place

### Rules — read every session
- Never rename anything
- Never touch baton_server/ without explicit instruction
- Never run plan mode unless asked
- Always verify with curl after docker changes
- Report only: what changed, verification output, errors

### Completed
- Docker boot
- baton.* package structure
- Full rename projskep → baton
- HTML integration at /
- WS keepalive
- Real metric:update gauge parsing
- Canonical repo structure
- README rewrite
- LICENSE
- GitHub Actions audit
- Archive non-runtime artifacts
- Legacy projskep reference cleanup

### Next tasks
1. Wire Ollama agents (langchain_ollama install in full image)
2. Add pre-commit hooks for commit discipline
