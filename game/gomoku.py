from game.game_base import Game
from board.board import Board
from utils.observer import Observable
from storage.file_manager import FileManager
from game.rules.win_condition import GomokuWinCondition
from game.rules.move_strategy import GomokuMoveStrategy

class Gomoku(Game, Observable):
    def __init__(self, board_size):
        Game.__init__(self, board_size)
        Observable.__init__(self)
        self.board = Board(board_size)
        self.players = ["X", "O"]
        self.gametype = "gomoku"
        # 使用传入的胜负判断策略，默认为 GomokuWinCondition
        self.win_condition = GomokuWinCondition()
        self.move_strategy = GomokuMoveStrategy()

    def make_move(self, player, position):
        """处理玩家落子"""
        x, y = position
        last_state = self._save_state(self.last_player,self.last_move)
        if self.move_strategy.make_move(self.board, x, y, player):
            self.history.append(last_state)  # 保存状态用于悔棋
            self.last_player = player
            self.last_move = (x,y)
            if self.win_condition.check_victory(self.board, x, y, player):
                self.winner = player
            else:
                # 检查是否平局
                if self.board.is_board_full():
                    self.winner = "X+O"
                    print("棋盘已满，平局！")
            self.current_player = (self.current_player + 1) % len(self.players)
            self.notify_observers()
            return True
        print("落子无效，请重新输入！")
        return False
