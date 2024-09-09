import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now())

    items = relationship("Item", back_populates="owner_user", cascade='all, delete')
  


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    dataset = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime)

    owner_user = relationship("User", back_populates="items")
    images = relationship("Image", back_populates="owner_item", cascade='all, delete')
    exercises = relationship("Exercise", back_populates="owner_exercise", cascade='all, delete')
  


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    is_main = Column(Boolean, default=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    owner_id = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.now())

    owner_item = relationship("Item", back_populates="images")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    dataset = Column(JSON)
    owner_id = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.now())

    owner_exercise = relationship("Item", back_populates="exercises")
    approaches = relationship("Approach", back_populates="owner_approach", cascade='all, delete')


class Approach(Base):
    __tablename__ = "approaches"

    id = Column(Integer, primary_key=True)
    ammount = Column(String, index=True)
    weight = Column(String, index=True, default=None)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    dataset = Column(JSON)
    owner_id = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.now())

    owner_approach = relationship("Exercise", back_populates="approaches")
 