from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import schemas
from fastapi_users import models as user_models
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable[str], Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
