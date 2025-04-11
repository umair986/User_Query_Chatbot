# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# with open(".env") as f:
#     print("\n🔍 RAW .env FILE:")
#     print(f.read())


# --- Required Config ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# --- Optional Config ---
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY", "GT")


# Validate required variables
required = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "MONGO_URI": MONGO_URI,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION_NAME": MONGO_COLLECTION_NAME,
}

missing = [key for key, val in required.items() if not val]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")


# print("✅ MONGO_URI:", MONGO_URI)
