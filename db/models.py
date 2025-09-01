from typing import List, Optional

from sqlalchemy import BigInteger, String, ForeignKey, Integer, Boolean, Numeric, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    feedback: Mapped[Optional[str]] = mapped_column(String(400))
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    portfolio_items: Mapped[List["Portfolio"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    alerts: Mapped[List["Alert"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))  # Внешний ключ!
    coin_id: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="portfolio_items")


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))  # Внешний ключ!
    coin_id: Mapped[str] = mapped_column(String)
    target_price: Mapped[float] = mapped_column(Float)
    condition: Mapped[str] = mapped_column(String(2))

    user: Mapped["User"] = relationship(back_populates="alerts")