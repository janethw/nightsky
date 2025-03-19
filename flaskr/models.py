from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from . import db


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
                  
                  
class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    # Ref: 'Many To One' @ https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-one
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # Ref: https://www.geeksforgeeks.org/ensuring-timestamp-storage-in-utc-with-sqlalchemy/
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    title: Mapped[str]
    body: Mapped[str]
    author: Mapped["User"] = relationship(back_populates="posts")


class Nasa(db.Model):
    __tablename__ = 'nasa'
    id: Mapped[int] = mapped_column(primary_key=True)
    url_apod: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    year_apod: Mapped[int] = mapped_column(nullable=False)
    month_apod: Mapped[int] = mapped_column(nullable=False)
    day_apod: Mapped[int] = mapped_column(nullable=False)
    explanation: Mapped[str]
    copyright: Mapped[str]
    hdurl: Mapped[str]
    media_type: Mapped[str]
