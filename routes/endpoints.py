from fastapi import APIRouter,HTTPException,status,Depends,Response
from models.user_model import register,UpdateUser
from schema.database import db
from hashing import hashingpassword
import json
from bson import ObjectId
from routes.passwordcheck import checkpassword
from Oauth2 import get_current_user_from_cookie
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt
from jwt_token_module import SECRET_KEY,ALGORITHM

pwd_encrypt = CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(
    prefix="/user"
)

collection=db["users"]

class JSONEncode(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,ObjectId):
            return str(o)
        return super().default(o)

@router.get("/",tags=["Database connection"])
def dbs():
    return "connected to mongo"

#User-Registration
@router.post("/Register/",tags=["User-Management"])
def user_registration(user:register):
    exist = collection.find_one({"username":user.username})
    if exist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user already exists")
    print(exist)
    user_dict=user.dict()
    if not checkpassword(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" password must be  at least 8 characters long, include uppercase, lowercase, number, and special character.")
    hashedpassword=hashingpassword(user_dict["password"])
    user_dict["password"] = hashedpassword
    result = collection.insert_one(user_dict)
    if not result:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE,detail = "please enter username and password")
    return "registered successfully"

#User-Login
@router.post("/Login/",tags=["User-Management"])
def user_login(response: Response,user:OAuth2PasswordRequestForm = Depends()):
    result=collection.find_one({"username":user.username}) 
    print(result)
    if not result or not pwd_encrypt.verify(user.password,result["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username or password is incorrect. Please try it again")
    token_data = {
        "sub": result["username"],
        "exp": datetime.utcnow() + timedelta(hours=2)  # token valid for 2 hours
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict" # prevent access from JavaScript
    )
    return {"message": "Login successful", "username": result["username"]}

#Update the user details
@router.put("/Update-Details/",tags=["User-Management"])
def updating_details(update_data : UpdateUser,current_user: str = Depends(get_current_user_from_cookie)):
    update_dict = update_data.dict()
    
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No data provided for update")
    
    if "password" in update_dict:
        if not checkpassword(update_dict["password"]):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="password must be atleast 8 characters with numbers and special characters")
        update_dict["password"]=hashingpassword(update_dict["password"])
    result = collection.update_one({"username":current_user},{"$set": update_dict})
    
    if not result:
        return {"message":"No changes made"}
    return {"message":"updated successfully"}

#logging out
@router.get("/Logout/",tags=["User-Management"])
def logout(response:Response):
    response.delete_cookie("access_token")
    return {"message":"logged out successfully"}    
    
    