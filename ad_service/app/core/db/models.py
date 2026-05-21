from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.database import Base


class Ad(Base):
    __tablename__ = "ads"

    ad_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    chats: Mapped[list["Chat"]] = relationship(back_populates="ad", cascade="all, delete-orphan")
    categories: Mapped[list["Category"]] = relationship(
        back_populates="ad", cascade="all, delete-orphan"
    )
    photos: Mapped[list["Photo"]] = relationship(back_populates="ad", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.ad_id", ondelete="CASCADE"), nullable=False)

    ad: Mapped["Ad"] = relationship(back_populates="categories")


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.ad_id", ondelete="CASCADE"), nullable=False)

    ad: Mapped["Ad"] = relationship(back_populates="photos")


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.ad_id", ondelete="CASCADE"), nullable=False)
    initiator_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    ad: Mapped["Ad"] = relationship(back_populates="chats")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    msg_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
