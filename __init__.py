print("Initializing Bank Utilities Nodes")
import os
from dotenv import load_dotenv

# Get the current directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')

print(f"Looking for .env file at: {env_path}")
if os.path.exists(env_path):
    print(f".env file found at: {env_path}")
    load_dotenv(env_path)
    print("Environment variables loaded from .env file")
    # Check if MONGO_URI is now available (without printing the full URI for security)
    mongo_uri = os.environ.get("MONGO_URI", "")
    if mongo_uri:
        print(f"MONGO_URI found, starts with: {mongo_uri[:10]}...")
    else:
        print("MONGO_URI not found in environment variables")
else:
    print(f"Warning: No .env file found at {env_path}")
    load_dotenv()  # Try default loading method
    print("Attempted to load environment variables from default locations")

from .node_index import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]