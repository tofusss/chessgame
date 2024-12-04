from game.game_base import Game
from board.board import Board
from utils.observer import Observable
from game.rules.move_strategy import GoMoveStrategy
from game.rules.win_condition import GoWinCondition

class Go(Game):
    def __init__(self, board_size):
        Game.__init__(self, board_size)
        Observable.__init__(self)
        self.board = Board(board_size)
        self.players = ["X", "O"]
        self.captures = {"X": 0, "O": 0}  # 提子计数
        self.pass_count = 0  # 连续虚着次数
        self.gametype = "go"
        # 使用传入的落子策略和胜负判断策略
        self.move_strategy = GoMoveStrategy()
        self.win_condition = GoWinCondition()

    def make_move(self, player, position):
        """处理玩家落子"""
        self.pass_count = 0  # 重置连续虚着计数
        x, y = position
        last_state = self._save_state(self.last_player,self.last_move)
        if self.move_strategy.make_move(self.board, x, y, player):
            
            self.history.append(last_state)  # 保存状态用于悔棋
            self.last_player = player
            self.last_move = (x,y)
            # 更新提子计数（具体实现留在 MoveStrategy 中）
            # self.captures[player] += 提子数
            self.current_player = (self.current_player + 1) % len(self.players)
            self.notify_observers()
            self.check_available_moves()
            return True
        return False
    
    def check_available_moves(self):
        if not self.has_legal_moves():
            print(f"{self.players[self.current_player]}没有合法的落子点")
            self.pass_turn()
            if not self.has_legal_moves():
                print(f"{self.players[self.current_player]}没有合法的落子点")
                self.pass_turn()

    def has_legal_moves(self):
        """检查棋盘上是否有合法的落子点"""
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.move_strategy.is_valid_move(self.board, x, y, self.players[self.current_player]):
                    #print("have legal moves")
                    return True
        return False
    
    def pass_turn(self):
        """处理虚着"""
        self.pass_count += 1
        if self.pass_count >= 2:
            print("双方均虚着，游戏结束！")
            self.winner = self.win_condition.check_victory(self.board, self.captures)
        else:
            self.current_player = (self.current_player + 1) % len(self.players)
        self.notify_observers()

    