from ui.composite_component import CompositeComponent
from ui.leaf_components import OperationTips, StatusBar

from commands.command_base import Command
from commands.command_base import PassCommand
from commands.command_base import MoveCommand
from commands.command_base import UndoMoveCommand
from commands.command_base import ResignCommand
from commands.command_base import RestartGameCommand
class ConsoleUI:
    def __init__(self, game,game_type):
        self.game = game
        self.game.add_observer(self)  # 订阅游戏状态
        self.running = True
        # 创建界面组件
        self.root = CompositeComponent()
        self.tips = OperationTips(game_type)  # 根据游戏类型初始化提示
        self.status_bar = StatusBar(game)

        # 添加组件到根组件
        self.root.add(self.tips)
        self.root.add(self.status_bar)

        # 创建命令映射表
        self.command_map = {
            "move": MoveCommand(self.game),
            "undo": UndoMoveCommand(self.game),
            "resign": ResignCommand(self.game, self.game.players[self.game.current_player]),
            "restart": RestartGameCommand(self.game),
            "pass": PassCommand(self.game,game_type),
            "show": self.show_tips,
            "hide": self.hide_tips,
            "save": self.save_game,
            "load": self.load_game,
            "quit": self.quit_game,
        }
    def update(self):
        """响应游戏状态更新"""
        print("\n当前棋盘：")
        self.game.board.display()
        if self.game.is_game_over():
            print(f"游戏结束！获胜者是：{self.game.determine_winner()}")

    def run(self):
        """主交互逻辑"""
        self.game.initialize_board()
        while not self.game.is_game_over():
            self.root.display()  # 显示界面组件
            command = input("\n输入指令：").lower()
            # 查找并执行命令
            if command in self.command_map:
                action = self.command_map[command]
                if isinstance(action, Command):
                    action.execute()  # 如果是 Command 实例，则执行
                else:
                    action()  # 如果是函数（如 show/hide），直接调用
            else:
                print("无效的指令，请重新输入！")
            

    def show_tips(self):
            """显示操作提示"""
            self.tips.visible = True
            print("操作提示已显示。")

    def hide_tips(self):
        """隐藏操作提示"""
        self.tips.visible = False
        print("操作提示已隐藏。")

    def save_game(self):
        """保存游戏"""
        file_path = input("输入保存文件路径：")
        self.game.save_game(file_path)

    def load_game(self):
        """加载游戏"""
        file_path = input("输入加载文件路径：")
        self.game.load_game(file_path)

    def quit_game(self):
        """退出游戏"""
        print("游戏结束！")
        self.game.winner = "quit"  # 清理游戏状态