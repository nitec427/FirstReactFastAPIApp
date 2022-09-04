from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from pydantic import BaseModel
from datetime import datetime
from bson.objectid import ObjectId
app = FastAPI()

MONGO_DETAILS = "mongodb+srv://nitec_427:70657065@cluster0.m7lhg6y.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.FASTAPI

FASTAPI_collection = database.get_collection("TodoDB")

def schema_helper(task) -> dict:
    """Helper function to make mongo query dict"""
    
    return {
        "id": str(task["_id"]),
        "Date Created": task["created_date"],
        "Creator Name": task["creator"],
        "Title": task["title"],
        "Body": task["body"],
        "Duration": task["duration"],
    }
    
class Notes(BaseModel):
    created_date: str
    creator: str
    title: str
    body: str
    duration: str
    
origins = [
    "http://localhost:3000", "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/", tags = ["root"])
# async def read_root() -> dict:
#     return {"message", "Welcome to your to-do"}
@app.get("/todo")
async def get_todos() -> dict:
    todos = []
    async for todo in FASTAPI_collection.find():
        todos.append(schema_helper(todo))
    return todos

@app.get("/{data_id}")
async def get_data(data_id:str):
    data_data = await FASTAPI_collection.find_one({"_id": ObjectId(data_id)})
    return schema_helper(data_data)


@app.post('/todo')
async def post_data(item:dict ) -> dict:
    data_data = await FASTAPI_collection.insert_one(item)
    new_data = await FASTAPI_collection.find_one({"_id": ObjectId(data_data.inserted_id)})
    return schema_helper(new_data)

@app.delete('delete_data/{data_id}')
async def delete_data(data_id:str):
    data = await FASTAPI_collection.find_one({"_id": ObjectId(data_id)})
    if data:
        await FASTAPI_collection.delete_one({"_id": ObjectId(data_id)})
        return True
    return False

@app.put('/update_data/{data_id}')
async def update_data(id: str, data:dict):
    if len(data) < 1:
        return False
    
    data = await FASTAPI_collection.find_one({"_id": ObjectId(id)})
    data.update({"update":True, "updated_time":datetime.now()})
    if data:
        updated_data = await FASTAPI_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_data:
            return True
        return False