import json
from player.player_account import PlayerAccount
class AccountStorage:
    FILE_PATH = "accounts.json"

    @staticmethod
    def load_accounts():
        try:
            with open(AccountStorage.FILE_PATH, 'r') as f:
                data = json.load(f)
                return {
                    username: PlayerAccount.from_dict(info)
                    for username, info in data.items()
                }
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_accounts(accounts):
        with open(AccountStorage.FILE_PATH, 'w') as f:
            data = {username: account.to_dict() for username, account in accounts.items()}
            json.dump(data, f)