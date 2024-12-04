from player.player import GuestPlayer
from player.player import RegisteredPlayer
from player.player import AIPlayer

class PlayerFactory:
    _guest_counter = 0

    @staticmethod
    def create_guest():
        PlayerFactory._guest_counter += 1
        return GuestPlayer(PlayerFactory._guest_counter)

    @staticmethod
    def create_registered(account):
        return RegisteredPlayer(account)
    
    @staticmethod
    def create_ai(ai_level=1):
        return AIPlayer(ai_level)