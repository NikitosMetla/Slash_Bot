from datetime import datetime
from typing import Sequence

from sqlalchemy import select, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Users


class UserRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_user(self, user_id: int, username: str, donate: bool, attempts: int = 3):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = Users(user_id=user_id, username=username, attempts=attempts, donate=donate)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_user_by_user_id(self, user_id: int) -> Users:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users).where(or_(Users.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_users(self) -> Sequence[Users]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users)
                query = await session.execute(sql)
                return query.scalars().all()

    async def delete_attempt_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = update(Users).values({
                    Users.attempts: Users.attempts - 1
                }).where(or_(Users.user_id == user_id))
                await session.execute(sql)
                await session.commit()

    async def give_attempts_by_user_id(self, user_id: int, attempts: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                new_attempts = Users.attempts + attempts
                sql = update(Users).values({
                    Users.attempts: new_attempts
                }).where(or_(Users.user_id == user_id))
                await session.execute(sql)
                await session.commit()

    async def update_donate_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = update(Users).values({
                    Users.donate: True
                }).where(or_(Users.user_id == user_id))
                await session.execute(sql)
                await session.commit()




    # async def update_user_update_date_by_user_id(self, user_id: int):
    #     async with self.session_maker() as session:
    #         session: AsyncSession
    #         async with session.begin():
    #             date_now = datetime.now()
    #             sql = update(Users).values({
    #                 Users.upd_date: date_now
    #             }).where(or_(Users.id == user_id))
    #             await session.execute(sql)
    #             await session.commit()



