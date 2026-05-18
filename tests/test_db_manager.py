import pytest
import pytest_asyncio
from baton_server.db.manager import init_db, log_trace


@pytest.mark.asyncio
async def test_init_db_creates_tables():
    await init_db()
    assert True


@pytest.mark.asyncio
async def test_log_trace_inserts():
    await init_db()
    await log_trace("TEST", "test message", {"key": "value"})
    assert True
