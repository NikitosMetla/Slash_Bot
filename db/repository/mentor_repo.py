from datetime import datetime
from typing import Sequence

from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Mentor


class MentorRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_mentor(self, user_id: int, last_date_start: datetime):
        """
        user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
        user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = Mentor(user_id=user_id, last_start_date=last_date_start)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_user_by_user_id(self, user_id: int) -> Mentor:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Mentor).where(or_(Mentor.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_users(self) -> Sequence[Mentor]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Mentor)
                query = await session.execute(sql)
                return query.scalars().all()

    async def update_user_last_start_date_by_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                date_now = datetime.now()
                sql = update(Mentor).values({
                    Mentor.last_start_date: date_now
                }).where(or_(Mentor.user_id == user_id))
                await session.execute(sql)
                await session.commit()


