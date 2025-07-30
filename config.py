import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# MongoDB Configuration
MONGO_USERNAME = os.getenv("MONGO_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DBNAME = os.getenv("MONGO_DBNAME", "health_app")

# For local MongoDB
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"

# Optional: For MongoDB Atlas (cloud-hosted)
# MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority"

# Flask secret key
SECRET_KEY = os.getenv("SECRET_KEY", "abc123")
