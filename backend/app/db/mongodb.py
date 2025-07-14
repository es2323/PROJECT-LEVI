from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get the MongoDB URI from environment variables
URI = os.getenv("MONGODB_URI")
if not URI:
    raise ValueError("MONGODB_URI environment variable is not set.")
# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))

# Ping the server to confirm connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise  # Re-raise to handle connection issues upstream

# Get the database and collection
db = client["levi"]
collection = db["users"]

# Function to get the collection (for reuse in the app)
def get_collection():
    return collection

# Function to close the client (to be called when the app shuts down)
def close_connection():
    client.close()

if __name__ == "__main__":
    # Example usage for testing
    from backend.app.models.user import user_example  # Adjust path as needed
    try:
        result = collection.insert_one(user_example)
        print(f"Example user inserted with id: {result.inserted_id}")
        user = collection.find_one({"skills": "python"})
        if user:
            print(f"Example user found: {user}")
        else:
            print("No example user found.")
    except Exception as e:
        print(f"Error during example operation: {e}")
    finally:
        close_connection()
