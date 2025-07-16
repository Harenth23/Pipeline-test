import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

# Fetch Mongo URI from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Initialize MongoDB client
try:
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.todo_db
except ServerSelectionTimeoutError as e:
    print(f"Error: Could not connect to MongoDB at {MONGO_URI}")
    raise e

# Return database instance (used in route handlers or dependency injection)
def get_db():
    return db
