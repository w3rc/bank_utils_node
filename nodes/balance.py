import os
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bank_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
accounts_collection = db["accounts"]


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
            response = f"${amount_int} transferred from {source_user_id} to {target_user_id}"
            return (response,)
        except ValueError:
            return ("Invalid amount",)
        except Exception as e:
            return ((f"An error occurred during transfer: {str(e)}",),)