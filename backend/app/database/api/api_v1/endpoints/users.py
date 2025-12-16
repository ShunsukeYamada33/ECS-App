from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.schemas.user import UserCreate, UserRead
from app.database.crud.user import get_user_by_email, create_user, get_user
from app.database.db.session import AsyncSessionLocal

router = APIRouter()


# dependency to get a DB session for a request
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/users/", response_model=UserRead)
async def api_create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_in)
    return user


@router.get("/users/{user_id}", response_model=UserRead)
async def api_get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    u = await get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u
