from typing import Iterable, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from databases import Database
from sqlalchemy.dialects.postgresql import insert as pg_insert

from authx.database import BaseDBBackend


class EncodeDBBackend(BaseDBBackend):
    """Setup Database for authx using Encode Database (SQLAlchemy Core)"""

    def __init__(
        self, database: Database, users: sa.Table, email_confirmations: sa.Table
    ) -> None:
        self.users = users
        self.email_confirmations = email_confirmations
        self.database = database

    async def get(self, id: UUID) -> Optional[dict]:
        query = sa.select(self.users).where(self.users.c.id == id)
        return await self.database.fetch_one(query)

    async def get_by_email(self, email: str) -> Optional[dict]:
        query = sa.select(self.users).where(self.users.c.email == email)
        return await self.database.fetch_one(query)

    async def get_by_username(self, username: str) -> Optional[dict]:
        query = sa.select(self.users).where(self.users.c.username == username)
        return await self.database.fetch_one(query)

    async def get_by_social(self, provider: str, sid: str) -> Optional[dict]:
        query = (
            sa.select(self.users)
            .where(self.users.c.provider == provider)
            .where(self.users.c.sid == sid)
        )
        return await self.database.fetch_one(query)

    async def create(self, obj: dict) -> UUID:
        uuid = uuid4()
        obj[id] = uuid
        query = self.users.insert()
        await self.database.execute(query=query, values=obj)
        return uuid

    async def update(self, id: UUID, obj: dict) -> bool:
        # TODO: Take care to remove any existing ID
        obj.pop("id", None)

        query = (
            sa.update(self.users)
            .where(self.users.c.id == id)
            .values(obj)
            .returning(self.users.c.id)
        )
        res = await self.database.execute(query)
        return bool(res)

    async def delete(self, id: UUID) -> bool:
        query = (
            sa.delete(self.users)
            .where(self.users.c.id == id)
            .returning(self.users.c.id)
        )
        res = await self.database.execute(query)
        return bool(res)

    async def count(self, query: Optional[dict] = None) -> int:
        # TODO: Fix Query is ignored
        query = sa.select(sa.func.count()).select_from(self.users)
        return await self.database.fetch_one(query)

    async def request_email_confirmation(self, email: str, token_hash: str) -> None:
        query = (
            pg_insert(self.email_confirmations)
            .values(email=email, token=token_hash)
            .on_conflict_do_update(constraint="email", set_={"token": token_hash})
        )
        await self.database.execute(query)
        return None

    async def confirm_email(self, token_hash: str) -> bool:
        query = sa.select(self.email_confirmations).where(
            self.email_confirmations.c.token == token_hash
        )
        email_confirmation = await self.database.fetch_one(query)
        if email_confirmation:
            email = email_confirmation["email"]
            async with self.database.transaction():
                query = (
                    sa.update(self.users)
                    .where(self.users.c.email == email)
                    .values(confirmed=True)
                )
                await self.database.execute(query)
                query = sa.delete(self.email_confirmations).where(
                    self.email_confirmations.c.email == email
                )
                await self.database.execute(query)
            return True
        else:
            return False

    async def get_blacklist(self) -> Iterable[dict]:
        query = sa.select(self.users).where(self.users.c.active == False)
        return await self.database.fetch_all(query)

    async def search(self, f: dict, p: int, size: int) -> tuple[dict, int]:
        count = self.count(f)
        # TODO: FIX Query is ignored
        query = sa.select(self.users).offset((p - 1) * size).limit(size)
        users = await self.database.fetch_all(query)
        return users, count
