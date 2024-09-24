from datetime import datetime
from typing import Sequence

from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import DesignLevel


class DesignLevelRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_design_level(self, user_id: int, finish_service: bool, last_date_start: datetime):
        """
        user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
        finish_service = Column(Boolean, nullable=False)
        user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = DesignLevel(user_id=user_id, finish_service=finish_service, last_start_date=last_date_start)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_user_by_user_id(self, user_id: int) -> DesignLevel:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(DesignLevel).where(or_(DesignLevel.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_users(self) -> Sequence[DesignLevel]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(DesignLevel)
                query = await session.execute(sql)
                return query.scalars().all()

    async def update_user_last_start_date_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                date_now = datetime.now()
                sql = update(DesignLevel).values({
                    DesignLevel.last_start_date: date_now
                }).where(or_(DesignLevel.user_id == user_id))
                await session.execute(sql)
                await session.commit()


    async def update_finish_service_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = await self.get_user_by_user_id(user_id)
                if user.finish_service:
                    sql = update(DesignLevel).values({
                        DesignLevel.finish_service: False
                    }).where(or_(DesignLevel.user_id == user_id))
                    await session.execute(sql)
                    await session.commit()
                else:
                    sql = update(DesignLevel).values({
                        DesignLevel.finish_service: True
                    }).where(or_(DesignLevel.user_id == user_id))
                    await session.execute(sql)
                    await session.commit()


