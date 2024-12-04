from ui.component import Component

class OperationTips(Component):
    """操作提示组件"""
    def __init__(self, game_type):
        super().__init__()
        self.game_type = game_type
        self.tips = self._generate_tips()

    def _generate_tips(self):
        """根据游戏类型生成提示内容"""
        base_tips = [
            "move: 落子 (格式: x, y)",
            "undo: 悔棋",
            "resign: 认负",
            "restart: 重新开始",
            "show: 显示提示",
            "hide: 隐藏提示",
            "save: 保存局面",
            "load: 加载局面",
            "quit: 退出游戏"
        ]
        if self.game_type == "go":
            base_tips.insert(0, "pass: 虚着")
        return base_tips

    def update_tips(self, game_type):
        """更新游戏类型并重新生成提示"""
        self.game_type = game_type
        self.tips = self._generate_tips()

    def display(self):
        """显示操作提示"""
        if self.visible:
            print("\n可用指令：")
            for tip in self.tips:
                print(f"  {tip}")

class StatusBar(Component):
    """状态栏组件"""
    def __init__(self, game):
        super().__init__()
        self.game = game

    def display(self):
        if self.visible:
            current_player = self.game.players[self.game.current_player]
            if self.game.current_player == 0:
                print(f"\n当前状态：轮到玩家 {self.game.player_[0].username} 落子({current_player})")
            else:
                print(f"\n当前状态：轮到玩家 {self.game.player_[1].username} 落子({current_player})")

class AccountBar(Component):
    """账户状态栏组件，显示玩家账户信息与战绩"""
    def __init__(self, game):
        super().__init__()
        self.game = game  # 游戏实例，包含 player1 和 player2

    def display(self):
        if self.visible:
            player1 = self.game.player_[0]
            player2 = self.game.player_[1]

            print("======== 账户状态栏 ========")
            # 显示玩家1账户信息
            print(f"玩家1: {player1.get_username()}")
            stats1 = player1.get_stats()
            print(f"总场次: {stats1['total_games']} | 胜场: {stats1['wins']}")

            # 显示玩家2账户信息
            print(f"玩家2: {player2.get_username()}")
            stats2 = player2.get_stats()
            print(f"总场次: {stats2['total_games']} | 胜场: {stats2['wins']}")
            print("===========================")