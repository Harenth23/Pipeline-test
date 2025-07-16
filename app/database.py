from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"

def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    return client.todo_db
