from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from uuid import UUID
import os

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from models import User, Base
from user_manager import get_user_manager
from schemas import UserCreate, UserUpdate, UserRead
from matcher import match_resume_to_job

# --- Load environment variables ---
load_dotenv()
SECRET = os.getenv("SECRET")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# --- FastAPI app ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Database engine ---
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# --- Authentication backend ---
cookie_transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# --- User DB dependency ---
async def get_user_db(session: AsyncSession = Depends(async_session)):
    yield SQLAlchemyUserDatabase(User, session)

# --- FastAPIUsers setup ---
fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)



current_user = fastapi_users.current_user()

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/match", response_class=HTMLResponse)
async def match_resume(
    request: Request,
    resume: str = Form(...),
    job: str = Form(...),
    user: User = Depends(current_user),  # 🔒 Require auth
):
    score, breakdown = match_resume_to_job(resume, job)

    # TODO Week 4: Save to DB using user.id

    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": score,
        "interpretation": breakdown["interpretation"],
        "feedback": breakdown["feedback"],
        "resume": resume,
        "job": job
    })

from schemas import UserRead, UserCreate, UserUpdate

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
