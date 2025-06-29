from fastapi import  HTTPException,Request
# from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from schema.database import db
from jwt_token_module import SECRET_KEY,ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # adjust your login URL

collection = db["users"]

def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")