from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# 非同期エンジン
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# AsyncSession の factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# ユーティリティ: 非同期でテーブル作成（起動時に使う）
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
