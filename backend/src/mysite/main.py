import os
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

# MongoDB connection
MONGODB_CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]
client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client.todolist
todos_collection = db.todos

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    content: str


class TodoItemCreate(BaseModel):
    content: str


# POST - Create a todo
@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    new_todo = TodoItem(content=item.content)
    await todos_collection.insert_one(new_todo.model_dump(by_alias=True))
    return new_todo


# GET - Retrieve todos
@app.get("/todos", response_model=list[TodoItem])
async def get_todos():
    todos = await todos_collection.find().to_list(length=None)
    return todos


# DELETE - Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID):
    delete_result = await todos_collection.delete_one({"_id": todo_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully!"}
