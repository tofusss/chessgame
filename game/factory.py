from game.gomoku import Gomoku
from game.go import Go

class GameFactory:
    @staticmethod
    def create_game(game_type, board_size):
        if game_type == "gomoku":
            return Gomoku(board_size)
        
        elif game_type == "go":
            return Go(board_size)
        else:
            raise ValueError("不支持的游戏类型")