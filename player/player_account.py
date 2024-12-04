class PlayerAccount:
    def __init__(self, username, password):
        self.username = username
        self._password = password  # 加密存储
        self.total_games = 0
        self.wins = 0

    def verify_password(self, password):
        return self._password == password

    def update_stats(self, win):
        self.total_games += 1
        if win:
            self.wins += 1

    def to_dict(self):
        return {
            "username": self.username,
            "password": self._password,
            "total_games": self.total_games,
            "wins": self.wins,
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data["username"], data["password"])
        account.total_games = data["total_games"]
        account.wins = data["wins"]
        return account