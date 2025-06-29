from fastapi import APIRouter,HTTPException,status,Depends
from models.user_model import Tasks,OneTask
from schema.database import db 
from datetime import datetime
from Oauth2 import get_current_user_from_cookie
import json 
from bson.json_util import ObjectId,dumps
from fastapi.responses import JSONResponse
collection = db["operations"]

router=APIRouter()

class JSONEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,ObjectId):
            return str(o)
        return super().default(o)

#reading tasks
@router.post("/tasks/",tags=["Todo-operations"])
def create_task(task:Tasks, current_user: str = Depends(get_current_user_from_cookie)):
    task_data=task.dict()
    task_data["username"] = current_user
    task_data["created_at"] = str(datetime.utcnow())
    result = collection.insert_one(task_data)
    if not result.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="task not created")
    return {"message":"task created successfully"}

#read all tasks
@router.get("/tasks/",tags=["Todo-operations"])
def read_all(current_user: str = Depends(get_current_user_from_cookie)):
    tasks = list(collection.find({"username": current_user}))
    print(tasks)
    return json.loads(dumps(tasks))

#fetch specific task details
@router.post("/tasks/{by-title}",tags=["Todo-operations"])
def read_one(task:OneTask,current_user: str = Depends(get_current_user_from_cookie)):
    tasks=collection.find_one({"title":task.title,"username":current_user})
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Tasks were Found....")
    tasks["_id"] = str(tasks["_id"])
    return JSONResponse(content=tasks)

#updating the task details
@router.put("/tasks/{title}",tags=["Todo-operations"])
def updating_task_details(title : str,task:Tasks,current_user : str = Depends(get_current_user_from_cookie)):
    result = collection.find_one({"title":title,"username":current_user})
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No tasks are found to update")
    update_data=task.dict(exclude_unset=True) #updating only the provided fields
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No data provided to udpate")
    if "created_at" in update_data:
        update_data["created_at"]=str(datetime.utcnow())
    r = collection.update_one({"title":title,"username":current_user},{"$set": update_data})
    if not r:
        raise HTTPException(status_code = status.HTTP_304_NOT_MODIFIED,detail = "Not modified")
    return {"message" : "updated successfully"}
    
    
#delete specific task by title
@router.delete("/tasks/{by title}",tags=["Todo-operations"])
def delete_one(task:OneTask,current_user: str = Depends(get_current_user_from_cookie)):
    tasks = collection.delete_one({"username":current_user,"title":task.title})
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return {"message":f"{tasks} deleted successfully"}


#delete all tasks
@router.delete("/tasks/all",tags=["Todo-operations"])
def delete_all(current_user: str = Depends(get_current_user_from_cookie)):
    tasks = collection.delete_many({"username":current_user}) 
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="tasks are not found to delete")
    
    return {"message":"all tasks are deleted successfully"}   
    
    