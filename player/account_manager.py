from storage.account_storage import AccountStorage
from player.player_account import PlayerAccount
class AccountManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.accounts = AccountStorage.load_accounts()
        return cls._instance

    def register(self, username, password):
        if username in self.accounts:
            raise ValueError("Username already exists!")
        self.accounts[username] = PlayerAccount(username, password)
        self.save()

    def login(self, username, password):
        account = self.accounts.get(username)
        if account:
            if account.verify_password(password):
                return account
            else:
                raise ValueError("Invalid username or password!")
        else:
            print(f"用户 '{username}' 不存在，正在创建新账户...")
            self.register(username, password)  # 自动注册
            return self.accounts[username]

    def save(self):
        AccountStorage.save_accounts(self.accounts)