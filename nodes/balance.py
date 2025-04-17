class FetchBankBalance:
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

    def fetch_bank_balance(self, user_id):
        return str(int(99999))


class TransferBalance:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_user_id": ("STRING", {"forceInput": True}),
                "source_user_id": ("STRING", {"forceInput": True}),
                "amount": ("INT", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)  
    RETURN_NAMES = ("status",)
    FUNCTION = "transfer_bank_balance"

    def transfer_bank_balance(self, target_user_id, source_user_id, amount):
        response = f"${amount} transferred from {source_user_id} to {target_user_id}"
        return response