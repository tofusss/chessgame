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
            print(f"\n当前状态：轮到玩家 {current_player} 落子")