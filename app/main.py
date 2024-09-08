from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from .routers import user , post , auth , vote
from .database import engine , get_db
from . import  models
from .config import settings

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#origins=['https://www.google.com']
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def hello():
    return {"message" : "hello world"}