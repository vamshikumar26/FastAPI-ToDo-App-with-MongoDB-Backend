from datetime import datetime,timedelta,timezone
from jose import JWTError
import jwt
from models import user_model

SECRET_KEY="paste your token here"
ALGORITHM="by default use HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60 

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verifing the logged in token with secret key
def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_model.TokenData(username=username)
    except JWTError:
        raise credentials_exception