from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["filestorebot"]
collection = db["files"]

async def save_file(file_id, file_name):
    await collection.insert_one({
        "file_id": file_id,
        "file_name": file_name
    })

async def get_file_by_id(file_id):
    return await collection.find_one({"file_id": file_id})
