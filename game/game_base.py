from abc import ABC, abstractmethod
from storage.file_manager import FileManager
from board.board import Board
from utils.observer import Observable

class Game(ABC,Observable):
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = None  # 棋盘对象
        self.players = []  # 玩家列表
        self.current_player = 0
        self.history = []  # 用于悔棋功能
        self.winner = None
        self.undotimes = 2
        self.gametype = None


    def initialize_board(self):
        """初始化棋盘"""
        self.board = Board(self.board_size)
        self.history.clear()
        self.winner = None
        self.current_player = 0
        print("游戏重新开始！")
        self.notify_observers()


    @abstractmethod
    def make_move(self, player, position):
        """处理玩家的落子"""
        pass


    def display_board(self):
        """显示棋盘"""
        if self.board:
            self.board.display()
    
    def undo_move(self):
        """悔棋功能"""
        if not self.history:
            print("无棋可悔！")
            return
        if not self.undotimes:
            print("悔棋次数用尽")
            return
        last_state = self.history.pop()
        self._load_state(last_state)
        print("悔棋成功！")
        self.undotimes -= 1
        self.notify_observers()

    def resign(self):
        """认输功能"""
        self.winner = self.players[(self.current_player + 1) % len(self.players)]
        print(f"玩家 {self.players[self.current_player]} 认输！")
        self.notify_observers()

    def is_game_over(self):
        return self.winner is not None

    def determine_winner(self):
        return self.winner

    def _save_state(self):
        """保存当前状态"""
        return {
            "board": [row[:] for row in self.board.grid],
            "current_player": self.current_player,
            "winner": self.winner
        }

    def _load_state(self, state):
        """加载保存的状态"""
        self.board.grid = state["board"]
        self.current_player = state["current_player"]
        self.winner = state["winner"]

    def save_game(self, file_path):
        """保存局面"""
        data = {
            "board": [row[:] for row in self.board.grid],  # 棋盘状态
            "current_player": self.current_player,
            "players": self.players,
            "winner": self.winner,
            "history": [state for state in self.history]  # 历史记录
        }
        FileManager.save_to_file(file_path, data)

    def load_game(self, file_path):
        """加载局面"""
        data = FileManager.load_from_file(file_path)
        if data:
            self.board.grid = data["board"]
            self.current_player = data["current_player"]
            self.players = data["players"]
            self.winner = data["winner"]
            self.history = data["history"]
            self.notify_observers()