from game.gomoku import Gomoku
from game.go import Go
from game.reversi import Reversi
        
class GameFactory:
    @staticmethod
    def create_game(game_type, board_size=None):
        if game_type == "gomoku":
            return Gomoku(board_size)
        elif game_type == "go":
            return Go(board_size)
        elif game_type == "reversi":
            return Reversi(board_size)
        else:
            raise ValueError(f"不支持的游戏类型: {game_type}")
        