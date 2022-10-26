import asyncio
import datetime
from typing import Tuple

import pytest_asyncio
from sqlalchemy import create_engine, insert

from db.user_model import metadata_obj, get_db, users
from services.auth_service import AuthService
from schemas.user_schema import User
from databases import Database
from pytest import fixture
from starlette.testclient import TestClient
import app

TEST_DB = "postgresql://postgresUser:mysecretpassword@localhost:5432/test_db"

engine = create_engine(TEST_DB, echo=True)
database = Database(TEST_DB)


def connect_test_db():
    def get_test_db():
        return database

    app.get_db = get_test_db
    app.app.dependency_overrides[get_db] = get_test_db
    metadata_obj.create_all(engine)
    return get_test_db()


def disconnect_test_db():
    metadata_obj.drop_all(engine)


@fixture(scope='session', autouse=True)
def start_db():
    connect_test_db()
    yield
    disconnect_test_db()


@fixture(autouse=True)
def clear_table():
    for table in metadata_obj.tables:
        engine.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(table))


@fixture(scope='module')
def test_client():
    with TestClient(app.app) as client:
        yield client


@fixture()
def create_user_db():
    stmt = insert(users).values(username="Test1", password=AuthService.hash_password("password"))
    engine.execute(stmt)


@fixture()
def create_token() -> Tuple[dict, User]:
    auth = AuthService()
    user = User(id=1, username='Test1', password='password')
    tokens = auth.create_jwt_tokens(user)
    return tokens, user


@fixture()
def create_invalid_token() -> Tuple[dict, User]:
    auth = AuthService(time_now=datetime.datetime.utcnow() - datetime.timedelta(days=999))
    user = User(id=1, username='Test1', password='password')
    tokens = auth.create_jwt_tokens(user)
    return tokens, user
