# chessgame/game/player.py
from abc import ABC, abstractmethod
import random

class Player(ABC):
    def __init__(self, username):
        self.username = username

    @abstractmethod
    def update_stats(self, win: bool):
        pass

    @abstractmethod
    def get_stats(self):
        pass

    def get_username(self):
        return self.username

class GuestPlayer(Player):
    def __init__(self, guest_id):
        super().__init__(f"Guest{guest_id}")
        self.total_games = 0
        self.wins = 0

    def update_stats(self, win: bool):
        pass

    def get_stats(self):
        return {"total_games": "N/A", "wins": "N/A"}

class RegisteredPlayer(Player):
    def __init__(self, account):
        super().__init__(account.username)
        self.account = account  # 引用 PlayerAccount 实例

    def update_stats(self, win: bool):
        self.account.update_stats(win)

    def get_stats(self):
        return {
            "total_games": self.account.total_games,
            "wins": self.account.wins,
        }
    
class AIPlayer(Player):
    def __init__(self, ai_level=1):
        super().__init__(f"AI Level_{ai_level}")
        self.ai_level = ai_level

    def make_move(self, game):
        """
        AI 自动落子逻辑：随机选择合法位置
        :param game: 当前游戏实例
        :return: 落子位置 (x, y)
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves available for AI.")
        if self.ai_level == 1:
            return random.choice(legal_moves)
        else:
            move = self.move_choice(game,legal_moves)
            return move

    def get_stats(self):
        # AI 无需统计胜场数据
        return {"total_games": "N/A", "wins": "N/A"}

    def update_stats(self, win: bool):
        pass

    def move_choice(self, game, legal_moves):
        """
        选择五子棋中得分最高的落子位置。
        :param game: 当前游戏实例
        :param legal_moves: 可选的合法位置列表 [(x1, y1), (x2, y2), ...]
        :return: 得分最高的落子位置 (x, y)
        """
        max_score = -1
        best_moves = []

        for move in legal_moves:
            x, y = move
            score = self.evaluate_position(game, x, y)
            if score > max_score:
                max_score = score
                best_moves = [move]  # 更新最佳位置
            elif score == max_score:
                best_moves.append(move)  # 同分则加入备选列表

        # 随机选择最佳得分位置之一
        return random.choice(best_moves)

    def evaluate_position(self, game, x, y):
        """
        评估在棋盘上位置 (x, y) 的得分。
        分数由在四个方向上连续的同色棋子数决定。
        :param game: 当前游戏实例
        :param x: 棋盘的列索引
        :param y: 棋盘的行索引
        :return: 该位置的分数
        """
        directions = [
            (1, 0),  # 水平向右
            (0, 1),  # 垂直向下
            (1, 1),  # 右下对角线
            (1, -1) # 左下对角线
        ]

        current_player = game.players[game.current_player]
        #board = game.board  
        board_size = game.board.size
        max_count = 0

        for dx, dy in directions:
            count = 1  # 包括当前点
            # 检查正向方向
            for step in range(1, 5):  # 最多考虑 4 步（五子棋）
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < board_size and 0 <= ny < board_size and game.board.grid[nx][ny] == current_player:
                    count += 1
                else:
                    break
            # 检查反向方向
            for step in range(1, 5):
                nx, ny = x - step * dx, y - step * dy
                if 0 <= nx < board_size and 0 <= ny < board_size and game.board.grid[nx][ny] == current_player:
                    count += 1
                else:
                    break
            max_count = max(max_count, count)

        return max_count
