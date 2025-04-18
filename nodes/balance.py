import os
from pymongo import MongoClient

# Get MongoDB URI from environment and ensure it has the proper format
MONGO_URI = os.environ.get("MONGO_URI", "")
if MONGO_URI and not (MONGO_URI.startswith("mongodb://") or MONGO_URI.startswith("mongodb+srv://")):
    MONGO_URI = f"mongodb://{MONGO_URI}"
    
# If MONGO_URI is still empty, provide a fallback or raise a more descriptive error
if not MONGO_URI:
    print("ERROR: MONGO_URI environment variable is not set or empty")
    print("Please ensure you have set MONGO_URI in your .env file")
else:
    print(f"MongoDB URI: {MONGO_URI}")

MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "bank-db")

# Connect to MongoDB with error handling
try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    # Test connection
    client.server_info()  # This will raise an exception if connection fails
    print(f"Successfully connected to MongoDB database: {MONGO_DB_NAME}")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    print(f"MONGO_URI value format: {MONGO_URI}... (partial for security)")
    # Initialize with None to handle gracefully in code
    client = None
    db = None
    print("Database connection failed. Please check your MongoDB URI and database name.")

# Define collections only if database connection is successful
if db is not None:
    accounts_collection = db["accounts"]
    transactions_collection = db["transactions"]
else:
    print("Database connection is not established. Collections will not be defined.")

class FetchBankBalance:
    def __init__(self):
        self.balance = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_id": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("balance",)
    FUNCTION = "fetch_bank_balance"
    CATEGORY = "Banking"

    def get_balance(self, user_id):
        if not user_id:
            return 0
        user = accounts_collection.find_one({"user_id": user_id})
        if not user:
            accounts_collection.insert_one({"user_id": user_id, "balance": 0})
            return 0
        return user.get("balance", 0)

    def fetch_bank_balance(self, user_id):
        balance = self.get_balance(user_id)
        return (str(balance),)

class FindUsersFromNamePartial:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name_partial": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("user_ids",)
    FUNCTION = "find_users_from_name_partial"

    def find_users_from_name_partial(self, name_partial):
        users = accounts_collection.find({"user_id": {"$regex": name_partial}})
        user_ids = [user["user_id"] for user in users]
        return (user_ids,)
    
class FindAllUsers:
    @classmethod
    def INPUT_TYPES(cls):
        return {}

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("user_ids",)
    FUNCTION = "find_all_users"

    def find_all_users(self):
        users = accounts_collection.find({})
        user_ids = [user["user_id"] for user in users]
        return (user_ids,)

class TransferBalance:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_user_id": ("STRING", {"forceInput": True}),
                "source_user_id": ("STRING", {"forceInput": True}),
                "amount": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)  
    RETURN_NAMES = ("status",)
    FUNCTION = "transfer_bank_balance"

    def transfer_bank_balance(self, target_user_id, source_user_id, amount):
        try:
            amount_int = int(amount)
            source = accounts_collection.find_one({"user_id": source_user_id})
            if not source or source.get("balance", 0) < amount_int:
                return ("Insufficient funds",)
            # perform transfer
            accounts_collection.update_one({"user_id": source_user_id}, {"$inc": {"balance": -amount_int}})
            accounts_collection.update_one({"user_id": target_user_id}, {"$inc": {"balance": amount_int}}, upsert=True)
            
            # log transaction
            transactions_collection.insert_one({
                "source_user_id": source_user_id,
                "target_user_id": target_user_id,
                "amount": amount_int
            })

            response = f"${amount_int} transferred from {source_user_id} to {target_user_id}"
            return (response,)
        except ValueError:
            return ("Invalid amount",)
        except Exception as e:
            return ((f"An error occurred during transfer: {str(e)}",),)