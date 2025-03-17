from sqlalchemy import BigInteger, Boolean, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from decouple import config

engine = create_async_engine(config('POSTGRESQL'), echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()


class BirthdayPerson(Base):
    __tablename__ = 'birthday_persons'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    full_name: Mapped[str] = mapped_column()
    birthday_day = mapped_column(Date)
    link: Mapped[str] = mapped_column()