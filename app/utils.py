from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")

def hash(passward : str):
    return pwd_context.hash(passward)

def verfiy_credentials(plain_passward,hashed_passward):
    return pwd_context.verify(plain_passward,hashed_passward)