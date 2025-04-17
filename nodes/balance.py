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


    def get_balance(self, user_id):
        # Simulate fetching balance from a database or API
        # For the sake of this example, we'll just return a fixed value
        return 99898

    def fetch_bank_balance(self, user_id):
        balance = self.get_balance(user_id)
        return (str(balance),)


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
            response = f"${amount_int} transferred from {source_user_id} to {target_user_id}"
            print(response)
            return (response,)  # Return as a tuple
        except ValueError:
            raise ValueError("Amount must be an integer.")
        except Exception as e:
            raise Exception(f"An error occurred during transfer: {str(e)}")