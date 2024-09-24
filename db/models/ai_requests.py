from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .users import Users


class AiRequests(BaseModel, CleanModel):
    """Таблица запросов к gpt"""
    __tablename__ = 'ai_requests'

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
    answer_ai = Column(String, nullable=False)
    photo_id = Column(String, nullable=False)

    @property
    def stats(self) -> str:
        """
       :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<{self.__tablename__}:{self.id}>"

    def __repr__(self):
        return self.__str__()
