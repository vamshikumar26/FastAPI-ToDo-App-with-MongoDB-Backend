from fastapi import FastAPI
from routes import endpoints
from routes import todos
app = FastAPI()

app.include_router(endpoints.router)

app.include_router(todos.router)