import pytest
from httpx import AsyncClient

from scripts.make_migrations import make_migrations, rollback_all_migrations
from src.app.app import app
from src.app.db import db


@pytest.fixture(autouse=True, scope='session')
def db_migrations():
    make_migrations()
    yield
    rollback_all_migrations()


@pytest.fixture()
async def db_connect():
    await db.connect()
    yield
    await db.disconnect()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
