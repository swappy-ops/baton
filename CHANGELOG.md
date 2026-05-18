# Changelog

## [Unreleased]

### Added
- One-command install (`install.sh`, `install.ps1`)
- One-command run (`run.sh`, `run.ps1`)
- `/api/metrics` endpoint for system observability
- Enhanced `/api/status` with database, WebSocket, and session info
- Comprehensive test suite (pytest)
- GitHub Actions CI (test, docker, lint, audit jobs)
- `docs/RUNTIME.md` — runtime truth audit
- `docs/DEPENDENCIES.md` — full import mapping
- `docs/ARCHITECTURE.md` — canonical architecture document
- `CONTRIBUTING.md` — development guidelines
- `KNOWN_LIMITATIONS.md` — known issues and workarounds
- `DEPLOY.md` — deployment guide

### Changed
- Archived prototype scripts to `archive/prototypes/`
- Archived React UI to `archive/baton_ui_react/` (uses incompatible socket.io-client)
- Archived legacy `projskep.db` to `archive/legacy_db/`
- Archived `integrations/projskep/` to `archive/`
- Archived task queue directories to `archive/task_queues/`
- Removed duplicate `docs/architecture.md`
- Cleaned all "projskep" references from active codebase
- Updated `.env.example` ChromaDB path
- Updated `.dockerignore` for current structure
- Updated GitHub Actions workflow to comprehensive CI

### Fixed
- Health check socket bug (triple nesting fixed)
- Test session directory permission handling

## [0.1.0] — Initial Release
- FastAPI server with WebSocket support
- Neural Observatory UI (vanilla HTML/CSS/JS)
- SQLite trace logging
- Session memory persistence
- Event bus with attention scoring
- Mock telemetry streams
- Docker support
- LangGraph agent package (baton/)
