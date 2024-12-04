from abc import ABC, abstractmethod
from storage.file_manager import FileManager
from board.board import Board
from utils.observer import Observable
from player.player import AIPlayer

class Game(ABC,Observable):
    def __init__(self, board_size):
        self.gametype = None
        self.board_size = board_size
        self.board = None  # 棋盘对象
        self.players = []  # 玩家列表
        self.current_player = 0
        self.history = []  # 用于悔棋功能
        self.winner = None
        self.undotimes = 2
        self.last_player = None
        self.last_move = None
        self.player_ = []  # Player 实例
        # self.player2 = None

    def initialize_board(self):
        """初始化棋盘"""
        self.board = Board(self.board_size)
        self.history.clear()
        self.winner = None
        self.last_player = None
        self.last_move = None
        self.current_player = 0
        self.notify_observers()
    
    def set_players(self,player1, player2):
        self.player_.append(player1)
        self.player_.append(player2)
        # self.player1 = player1
        # self.player2 = player2

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

    def _save_state(self,last_player,last_move):
        """保存当前状态"""
        return {
            "board": [row[:] for row in self.board.grid],  # 棋盘状态
            "current_player": self.current_player,         # 当前玩家
            "winner": self.winner,                         # 胜者信息
            "last_player": last_player,                   # 上一步的玩家
            "last_move": last_move                        # 上一步的落子位置
        }

    def _load_state(self, state):
        """加载保存的状态"""
        self.board.grid = state["board"]
        self.current_player = state["current_player"]
        self.winner = state["winner"]
        self.last_player = state["last_player"]
        self.last_move = state["last_move"]

    def save_game(self, file_path):
        """保存局面"""
        data = {
            "board": [row[:] for row in self.board.grid],  # 棋盘状态
            "board_size":self.board.size,
            "current_player": self.current_player,
            "players": self.players,
            "winner": self.winner,
            "history": [state for state in self.history],  # 历史记录
            "gametype": self.gametype ,
            "board_size": self.board_size ,
            "last_player": self.last_player ,
            "last_move": self.last_move,
            "player1": self.player_[0].username,
            "player2": self.player_[1].username
        }
        FileManager.save_to_file(file_path, data)

    def load_game(self, file_path):
        """加载局面"""
        data = FileManager.load_from_file(file_path)
        if self.gametype != data["gametype"]:
            print(f"游戏类型不符合,{self.gametype} != {data["gametype"]}")
            self.notify_observers()
            return
        if data:
            self.board.grid = data["board"]
            self.board.size = data["board_size"]
            self.current_player = data["current_player"]
            self.players = data["players"]
            self.winner = data["winner"]
            self.history = data["history"]
            self.gametype = data["gametype"]
            self.board_size = data["board_size"]
            self.last_player = data["last_player"]
            self.last_move = data["last_move"]
            self.notify_observers()

    def replay_game(self,file_path):
        """逐步回放游戏历史"""
        data = FileManager.load_from_file(file_path)
        if data:
            self.board.grid = data["board"]
            self.board.size = data["board_size"]
            self.current_player = data["current_player"]
            self.players = data["players"]
            self.winner = data["winner"]
            self.history = data["history"]
            self.gametype = data["gametype"]
            self.board_size = data["board_size"]
            self.last_player = data["last_player"]
            self.last_move = data["last_move"]
            player1 = data["player1"]
            player2 = data["player2"]

        print("开始回放对局...")
        self.history.append(self._save_state(self.last_player,self.last_move))
        for step in self.history:
            # 加载历史状态
            self._load_state(step)
            # 显示棋盘
            self.board.display()
            if "last_player" in step and "last_move" in step and self.last_player is not None:
                if self.last_player == self.players[0]:
                    print(f"{player1}({step['last_player']}) 落子于 {step['last_move']}")
                else:
                    print(f"{player2}({step['last_player']}) 落子于 {step['last_move']}")
            input("按任意键继续...")  # 等待用户输入
        
        print("回放结束。")


    def ai_turn(self):
        """
        AI 玩家，则自动落子。
        """
        if self.current_player == 0:
            move = self.player_[0].make_move(self)
        else:
            move = self.player_[1].make_move(self)
        print(move)
        self.make_move(self.players[self.current_player],move)

    def get_legal_moves(self):
        """
        返回当前棋盘的所有合法落子点。
        """
        # 假设 board 是一个二维数组，0 表示空位
        legal_moves = []
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.move_strategy.is_valid_move(self.board,x,y,self.players[self.current_player]):  # 0 表示空位
                    legal_moves.append((x, y))
        return legal_moves