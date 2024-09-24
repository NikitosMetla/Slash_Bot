from datetime import datetime
from typing import Sequence

from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import EarningsLevel


class EarningsLevelRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_earnings_level(self, user_id: int, finish_service: bool, last_date_start: datetime):
        """
        user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
        finish_service = Column(Boolean, nullable=False)
        user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = EarningsLevel(user_id=user_id, finish_service=finish_service, last_start_date=last_date_start)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_user_by_user_id(self, user_id: int) -> EarningsLevel:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(EarningsLevel).where(or_(EarningsLevel.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_users(self) -> Sequence[EarningsLevel]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(EarningsLevel)
                query = await session.execute(sql)
                return query.scalars().all()

    async def update_user_last_start_date_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                date_now = datetime.now()
                sql = update(EarningsLevel).values({
                    EarningsLevel.last_start_date: date_now
                }).where(or_(EarningsLevel.user_id == user_id))
                await session.execute(sql)
                await session.commit()

    async def update_finish_service_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = await self.get_user_by_user_id(user_id)
                if user.finish_service:
                    sql = update(EarningsLevel).values({
                        EarningsLevel.finish_service: False
                    }).where(or_(EarningsLevel.user_id == user_id))
                    await session.execute(sql)
                    await session.commit()
                else:
                    sql = update(EarningsLevel).values({
                        EarningsLevel.finish_service: True
                    }).where(or_(EarningsLevel.user_id == user_id))
                    await session.execute(sql)
                    await session.commit()


