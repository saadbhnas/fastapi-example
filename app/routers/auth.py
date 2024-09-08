from fastapi import FastAPI , APIRouter , Depends , HTTPException , status
from .. import schemas , database , models , utils , oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['login'])

@router.post('/login',response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(database.get_db)):
    #instead of user_credentials being set to userlogin schemas we can use fastapi OAuth2PasswordRequestForm which store two variables
    #username and passward for the username it could be the email but its just stored as username 
    #the right exception here is 403 

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="wrong credentials")
    
    verfiy_crdentials = utils.verfiy_credentials(user_credentials.password , user.passward)

    if not verfiy_crdentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="wrong credentials")
    
    token = oauth2.create_token(data={"user_id" : user.id})

    return {"token" : token , "token_type" : "bearer"}