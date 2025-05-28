from fastapi_users import BaseUserManager, UUIDIDMixin
from models import User
from typing import Optional
from uuid import UUID
from dotenv import load_dotenv
from fastapi import Request
import os

load_dotenv()
SECRET = os.getenv("SECRET")

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    user_db_model = User
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
async def get_user_manager(user_db):
    yield UserManager(user_db)