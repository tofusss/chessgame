from game.game_base import Game
from board.board import Board
from utils.observer import Observable
from game.rules.move_strategy import ReversiMoveStrategy

class Reversi(Game, Observable):
    def __init__(self,board_size = 8):
        super().__init__(board_size)  # 黑白棋默认棋盘大小为8*8
        Observable.__init__(self)
        self.board = Board(board_size)
        self.gametype = "reversi"
        self.players = ["B", "W"]  # 黑白棋玩家
        self.move_strategy = ReversiMoveStrategy()

    def initialize_board(self):
        """初始化棋盘，设置中心位置的棋子"""
        center = self.board.size // 2
        self.board.place_piece(center - 1, center - 1, "B")  # 左上角黑棋
        self.board.place_piece(center, center, "B")          # 右下角黑棋
        self.board.place_piece(center - 1, center, "W")      # 右上角白棋
        self.board.place_piece(center, center - 1, "W")      # 左下角白棋
        print("黑白棋棋盘已初始化")
        self.notify_observers()

    def make_move(self, player, position):
        """处理玩家落子"""
        x, y = position
        last_state = self._save_state(self.last_player,self.last_move)

        # 使用策略检查并执行落子逻辑
        if self.move_strategy.make_move(self.board, x, y, player):
            self.history.append(last_state)  # 保存状态用于悔棋
            self.last_player = player
            self.last_move = (x,y)
            #print("落子")
            if not self.has_legal_moves(self.players[(self.current_player + 1) % len(self.players)]):
                print(f"玩家 {self.players[(self.current_player + 1) % len(self.players)]} 无合法棋步，跳过回合！")
                self.current_player = (self.current_player + 1) % len(self.players)

            # 切换到下一玩家
            self.current_player = (self.current_player + 1) % len(self.players)

            # 检查游戏是否结束
            if not self.has_legal_moves("B") and not self.has_legal_moves("W"):
                self.winner = self.determine_winner()
            self.notify_observers()
            return True

        print("落子无效，请重新输入！")
        self.notify_observers()
        return False

    def has_legal_moves(self, player):
        """检查玩家是否有合法棋步"""
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.move_strategy.is_valid_move(self.board, x, y, player):
                    return True
        return False

    def determine_winner(self):
        """判断胜负"""
        black_count = sum(row.count("B") for row in self.board.grid)
        white_count = sum(row.count("W") for row in self.board.grid)
        print(f"黑棋数量: {black_count}, 白棋数量: {white_count}")
        if black_count > white_count:
            return "B"
        elif white_count > black_count:
            return "W"
        else:
            return "Draw"