from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    if not MONGO_URI:
        raise ValueError("No MONGO_URI found in .env file")
    client = MongoClient(MONGO_URI)
    # Use the default database from connection string, or fallback
    return client.get_database() 

def init_db():
    """MongoDB doesn't require explicit table creation, 
    but we can create the database connection and perhaps indexes if needed later."""
    db = get_db()
    # Ping to test connection
    db.command('ping')
    return db

if __name__ == "__main__":
    db = init_db()
    print("MongoDB connection initialized successfully:", db.name)
