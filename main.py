from fastapi import FastAPI
from database import engine, Base
from api import user_router

# สร้างตารางตาม models
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router จากแต่ละ module
app.include_router(user_router.router, prefix="/users", tags=["Users"])
