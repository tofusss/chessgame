from abc import ABC, abstractmethod
class Command(ABC):
    """命令基类，所有具体命令都应继承此类"""

    @abstractmethod
    def execute(self):
        """执行命令"""
        pass

class MoveCommand(Command):
    def __init__(self, game):
        self.game = game

    def execute(self):
        """调用游戏实例的悔棋方法"""
        try:
            position = input("输入落子位置 (x, y)：")
            x, y = map(int, position.split(","))
            self.game.make_move(self.game.players[self.game.current_player], (x, y))
        except ValueError:
            print("输入格式错误，请重新输入！")
class PassCommand(Command):
    def __init__(self, game,game_type):
        self.game = game
        self.game_type = game_type

    def execute(self):
        """调用游戏实例的虚着方法"""
        if self.game_type != "go":
            print("无效的指令，请重新输入！")
            return
        self.game.pass_turn()

class ResignCommand(Command):
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def execute(self):
        """执行认输逻辑"""
        self.game.winner = self.game.players[(self.game.players.index(self.player) + 1) % len(self.game.players)]
        print(f"玩家 {self.player} 投子认负，游戏结束！")

class RestartGameCommand(Command):
    def __init__(self, game):
        self.game = game

    def execute(self):
        """调用游戏实例的重新开始方法"""
        self.game.initialize_board()
        print("游戏已重新开始！")

class UndoMoveCommand(Command):
    def __init__(self, game):
        self.game = game

    def execute(self):
        """调用游戏实例的悔棋方法"""
        self.game.undo_move()