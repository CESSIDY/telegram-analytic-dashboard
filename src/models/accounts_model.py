from dataclasses import dataclass


@dataclass
class AccountsLoaderModel:
    api_id: int
    api_hash: str
    username: str

    def __init__(self, api_id: int, api_hash: str, username: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.username = username
