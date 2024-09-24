from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, BigInteger
from sqlalchemy.orm import Mapped, relationship

from db.base import CleanModel, BaseModel
from .users import Users


class SendLink(BaseModel, CleanModel):
    """
        модель уровня дизайна
    """
    __tablename__ = 'send_link'

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    last_start_date = Column(DateTime, nullable=False)
    user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')

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