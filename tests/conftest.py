from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest
import pytest_asyncio
from bson import ObjectId
from fastapi import FastAPI
import httpx

from app.routes.auth import router as auth_router
from app.routes.task import router as task_router


@dataclass
class InsertOneResult:
    inserted_id: ObjectId


@dataclass
class DeleteOneResult:
    deleted_count: int


@dataclass
class UpdateOneResult:
    matched_count: int
    modified_count: int


class FakeCursor:
    def __init__(self, docs: list[dict[str, Any]]):
        self._docs = docs
        self._iterator = iter(())

    def sort(self, key: str, direction: int):
        reverse = direction == -1
        self._docs = sorted(self._docs, key=lambda doc: doc.get(key), reverse=reverse)
        return self

    def __aiter__(self):
        self._iterator = iter(self._docs)
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration


class FakeCollection:
    def __init__(self):
        self._docs: list[dict[str, Any]] = []

    async def find_one(self, query: dict[str, Any]):
        for doc in self._docs:
            if _matches(doc, query):
                return dict(doc)
        return None

    async def insert_one(self, doc: dict[str, Any]):
        stored = dict(doc)
        stored.setdefault("_id", ObjectId())
        self._docs.append(stored)
        return InsertOneResult(inserted_id=stored["_id"])

    def find(self, query: dict[str, Any]):
        matches = [dict(doc) for doc in self._docs if _matches(doc, query)]
        return FakeCursor(matches)

    async def update_one(self, query: dict[str, Any], update: dict[str, Any]):
        set_data = update.get("$set", {})
        for index, doc in enumerate(self._docs):
            if _matches(doc, query):
                updated = dict(doc)
                updated.update(set_data)
                self._docs[index] = updated
                return UpdateOneResult(matched_count=1, modified_count=1)
        return UpdateOneResult(matched_count=0, modified_count=0)

    async def delete_one(self, query: dict[str, Any]):
        for index, doc in enumerate(self._docs):
            if _matches(doc, query):
                del self._docs[index]
                return DeleteOneResult(deleted_count=1)
        return DeleteOneResult(deleted_count=0)


class FakeDatabase:
    def __init__(self):
        self._collections = {
            "users": FakeCollection(),
            "tasks": FakeCollection(),
        }

    def __getitem__(self, name: str):
        return self._collections[name]


def _matches(doc: dict[str, Any], query: dict[str, Any]) -> bool:
    return all(doc.get(key) == value for key, value in query.items())


@pytest.fixture
def fake_db() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture
def unit_request(fake_db: FakeDatabase):
    return SimpleNamespace(app=SimpleNamespace(database=fake_db))


@pytest.fixture
def api_app(fake_db: FakeDatabase):
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(task_router)
    app.database = fake_db
    return app


@pytest_asyncio.fixture
async def client(api_app: FastAPI):
    transport = httpx.ASGITransport(app=api_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client
