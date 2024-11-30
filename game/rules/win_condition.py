from abc import ABC, abstractmethod

class WinCondition(ABC):
    @abstractmethod
    def check_victory(self, board, x, y, player):
        """
        检查当前玩家是否胜利
        :param board: 棋盘对象
        :param x: 落子位置的 x 坐标
        :param y: 落子位置的 y 坐标
        :param player: 当前玩家标记 ('X' 或 'O')
        :return: True 如果玩家胜利，否则 False
        """
        pass

class GomokuWinCondition(WinCondition):
    def check_victory(self, board, x, y, player):
        """
        检查五子连珠规则
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、对角线两方向
        for dx, dy in directions:
            count = 1  # 包含当前落子
            for step in (1, -1):  # 双向检查
                nx, ny = x, y
                while True:
                    nx, ny = nx + step * dx, ny + step * dy
                    if 0 <= nx < board.size and 0 <= ny < board.size and board.get_piece(nx, ny) == player:
                        count += 1
                        if count == 5:
                            return True
                    else:
                        break
        return False
    
class GoWinCondition(WinCondition):
    def check_victory(self, board, captures):
        """
        判断围棋胜负，基于地盘和提子数量的计分
        :param board: 棋盘对象
        :param captures: 提子计数，字典形式 {'X': 提子数, 'O': 提子数}
        :return: 胜利玩家 ('X' 或 'O') 或 None（平局）
        """
        black_score = captures['X'] + self.calculate_territory(board, 'X')
        white_score = captures['O'] + self.calculate_territory(board, 'O')

        print(f"黑方得分: {black_score}, 白方得分: {white_score}")

        if black_score > white_score:
            return 'X'
        elif white_score > black_score:
            return 'O'
        else:
            return 'X+O'

    def calculate_territory(self, board, player):
        """
        计算玩家的地盘大小
        :param board: 棋盘对象
        :param player: 玩家标记 ('X' 或 'O')
        :return: 地盘大小（空点数）
        """
        visited = set()
        territory = 0

        def dfs(x, y, owner):
            """
            深度优先搜索计算连通区域的所属权
            :param x: 起点 x 坐标
            :param y: 起点 y 坐标
            :param owner: 区域所属玩家标记 ('X', 'O') 或 None（中立）
            :return: (空点数, 所属玩家标记)
            """
            if (x, y) in visited or not (0 <= x < board.size and 0 <= y < board.size):
                return 0, owner
            visited.add((x, y))

            piece = board.get_piece(x, y)
            if piece == '.':  # 空点
                neighbors = self.get_neighbors(board, x, y)
                neighbor_owners = {board.get_piece(nx, ny) for nx, ny in neighbors if board.get_piece(nx, ny) != '.'}
                if len(neighbor_owners) == 1:
                    owner = next(iter(neighbor_owners))  # 区域所属唯一玩家
                else:
                    owner = None  # 中立区域
                return 1 + sum(dfs(nx, ny, owner)[0] for nx, ny in neighbors), owner
            elif piece == owner:
                neighbors = self.get_neighbors(board, x, y)
                return sum(dfs(nx, ny, owner)[0] for nx, ny in neighbors), owner
            else:
                return 0, None

        for x in range(board.size):
            for y in range(board.size):
                if (x, y) not in visited and board.get_piece(x, y) == '.':
                    area, owner = dfs(x, y, None)
                    if owner == player:
                        territory += area

        return territory

    def get_neighbors(self, board, x, y):
        """获取指定位置的邻居"""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < board.size and 0 <= ny < board.size]