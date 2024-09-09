from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.orm.database import engine
from app.routers import users, security, items, image, exercises, approaches
from app.orm import models



models.Base.metadata.create_all(bind=engine) #создание таблиц

# app = FastAPI(dependencies=[Depends(get_current_user)])
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(security.router)
app.include_router(items.router)
app.include_router(image.router)
app.include_router(exercises.router)
app.include_router(approaches.router)

