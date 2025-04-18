from .nodes.balance import FetchBankBalance, TransferBalance, FindAllUsers, FindUsersFromNamePartial

NODE_CLASS_MAPPINGS = {
    "FetchBankBalance": FetchBankBalance,
    "TransferBalance": TransferBalance,
    "FindAllUsers": FindAllUsers,
    "FindUsersFromNamePartial": FindUsersFromNamePartial
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FetchBankBalance": "Fetch Bank Balance",
    "TransferBalance": "Transfer Balance",
    "FindAllUsers": "Find All Users",
    "FindUsersFromNamePartial": "Find Users From Name Partial"
}
