from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db.session import init_db
from app.auth.router import router as auth_router
from app.api.router import router as api_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 起動時にテーブルを作成し DB に接続する準備を行う
@app.on_event("startup")
async def on_startup():
    await init_db()
