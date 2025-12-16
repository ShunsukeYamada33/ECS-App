from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.database.models.user import User
from app.database.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(db: AsyncSession, user_id: int):
    q = await db.execute(select(User).where(User.id == user_id))
    return q.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    q = await db.execute(select(User).where(User.email == email))
    return q.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise