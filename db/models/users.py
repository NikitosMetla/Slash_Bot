from sqlalchemy import Column, BigInteger, String, Boolean

from db.base import BaseModel, CleanModel


class Users(BaseModel, CleanModel):
    """
    Таблица юзеров
    """
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True, unique=False)
    donate = Column(Boolean, default=False, unique=False)
    attempts = Column(BigInteger, nullable=False, default=3)

    @property
    def stats(self) -> str:
        """
        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<{self.__tablename__}:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
