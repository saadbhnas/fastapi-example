from fastapi import FastAPI , Response , status ,HTTPException , Depends , APIRouter
from .. import schemas , utils , models
from typing import List
from ..database import engine , get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.post('/' , status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
def create_user(user:schemas.CreateUser , db:Session=Depends(get_db)):

    hashed_passward = utils.hash(user.passward)
    user.passward = hashed_passward

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}' , response_model=schemas.UserOut)
def get_user(id : int , db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND , detail=f"user with id {id} doesn't exist")
    
    return user