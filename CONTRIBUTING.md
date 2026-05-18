# Contributing to Baton

## Development Setup

1. Fork and clone the repository
2. Run `./install.sh` (or `.\install.ps1` on Windows)
3. Answer "Y" when asked to install the full ML stack
4. Run `./run.sh` to start the server

## Running Tests

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

## Code Style

We use Black for Python formatting:

```bash
pip install black
black baton_server/ baton/
```

## Pull Request Process

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass: `pytest tests/ -v`
4. Format code: `black baton_server/ baton/`
5. Submit PR with description of changes

## Architecture Decisions

- `baton_server/` is the core runtime. Changes here affect Docker and production.
- `baton/` is the optional agent orchestration layer. Requires full ML stack.
- Never rename existing files or directories.
- Never touch `baton_server/` without understanding the full dependency chain.

## Adding New API Endpoints

1. Add route to `baton_server/api/__init__.py`
2. Add tests to `tests/test_api.py`
3. Update API table in README.md
4. Update docs/ARCHITECTURE.md if the endpoint changes system behavior
