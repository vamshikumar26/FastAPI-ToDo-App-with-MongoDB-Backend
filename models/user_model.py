from pydantic import BaseModel
from typing import Optional,List

class register(BaseModel):
    username: str
    password: str
    phone_number: Optional[str] = None
     
class login(BaseModel):
    username: str
    password: str
          
class UpdateUser(BaseModel):
    username: Optional[str]=None
    password: Optional[str]=None
    phone_number: Optional[str]=None
    
class Tasks(BaseModel):
    title: str
    description: str
    status: List[str]
    
class OneTask(BaseModel):
    title: str
    

    