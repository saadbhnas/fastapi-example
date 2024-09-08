from jose import jwt , JWTError
from datetime import datetime , timedelta
from . import schemas , database , models
from fastapi import Depends , HTTPException , status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#this is from the fastapi docs https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/?h=oauth#global-view
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_token(data:dict):
    
    #to_encode here is to make sure we dont change the original data
    to_encode = data.copy()
    expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiration_time})
    #the update here enclode information that goes in the dict that we made in the path operation function in this case user_id + exp

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verfiy_access_token(token:str,credentials_exception):

    #this function decode the jwt and extract id verfiy that id match and in the right format using pydantic and information extrcated from database then return token_data and this function is called inside get_current_user function

    try:
    
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id == None :
            raise credentials_exception
    
        token_data = schemas.VerfiyToken(id=id)

    except JWTError:
        credentials_exception

    return token_data

def get_current_user(token : str = Depends(oauth2_schema) , db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail= "wrong credentials" , 
                                          headers={"WWW.Authenticate":"Bearer"})
    
    user_token = verfiy_access_token(token=token , credentials_exception=credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == user_token.id).first()
    
    return user

#so additionally get_current_user function meant to fetch the user in order to do some work with the information 
