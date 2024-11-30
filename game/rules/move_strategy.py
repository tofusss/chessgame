from abc import ABC, abstractmethod

class MoveStrategy(ABC):
    @abstractmethod
    def make_move(self, board, x, y, player):
        """
        处理玩家的落子操作
        :param board: 棋盘对象
        :param x: 落子位置的 x 坐标
        :param y: 落子位置的 y 坐标
        :param player: 当前玩家标记 ('X' 或 'O')
        :return: True 如果落子成功，否则 False
        """
        pass

class GomokuMoveStrategy(MoveStrategy):
    def make_move(self, board, x, y, player):
        """五子棋的落子规则"""
        if board.is_valid_position(x, y):
            board.place_piece(x, y, player)
            return True
        else:
            print("落子无效，位置已被占用或超出边界！")
            return False
        
class GoMoveStrategy(MoveStrategy):
    def make_move(self, board, x, y, player):
        """围棋的落子规则"""
        if not board.is_valid_position(x, y):
            print("落子无效，位置已被占用或超出边界！")
            return False

        # 临时放置棋子以检查合法性
        board.place_piece(x, y, player)
        if not self.has_liberty(board, x, y, player):
            print("落子无效，棋子无气！")
            board.move_piece(x, y, ".")  # 移除临时放置的棋子
            return False

        # 提子操作：移除对方无气的棋子
        self.capture_stones(board, x, y, player)

        # 检查自己的棋子是否仍然有气（防止自杀）
        if not self.has_liberty(board, x, y, player):
            print("落子无效，造成自杀！")
            board.move_piece(x, y, ".")  # 移除临时放置的棋子
            return False

        print(f"玩家 {player} 在 ({x}, {y}) 落子")
        return True

    def has_liberty(self, board, x, y, player):
        """判断指定位置的棋子是否有气"""
        visited = set()

        def dfs(nx, ny):
            if (nx, ny) in visited:
                return False
            visited.add((nx, ny))

            # 如果有空点，说明有气
            if board.get_piece(nx, ny) == ".":
                return True

            # 如果是当前玩家的棋子，继续检查其连通区域
            if board.get_piece(nx, ny) == player:
                neighbors = self.get_neighbors(board, nx, ny)
                return any(dfs(nx, ny) for nx, ny in neighbors)

            return False

        return dfs(x, y)

    def capture_stones(self, board, x, y, player):
        """提子操作：移除无气的对方棋子"""
        opponent = "X" if player == "O" else "O"
        visited = set()

        def dfs(nx, ny):
            if (nx, ny) in visited:
                return []
            visited.add((nx, ny))

            # 如果是对方棋子，检查其是否有气
            if board.get_piece(nx, ny) == opponent:
                neighbors = self.get_neighbors(board, nx, ny)
                if any(board.get_piece(nx, ny) == "." for nx, ny in neighbors):
                    return []  # 有气，不提子
                return [(nx, ny)] + [stone for nx, ny in neighbors for stone in dfs(nx, ny)]

            return []

        # 检查四周的对方棋子
        neighbors = self.get_neighbors(board, x, y)
        for nx, ny in neighbors:
            if board.get_piece(nx, ny) == opponent:
                captured_stones = dfs(nx, ny)
                for cx, cy in captured_stones:
                    board.move_piece(cx, cy, ".")  # 移除被提的棋子
                if captured_stones:
                    print(f"提掉 {len(captured_stones)} 枚棋子：{captured_stones}")

    def get_neighbors(self, board, x, y):
        """获取当前位置的邻居"""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < board.size and 0 <= ny < board.size]
    
    def is_valid_move(self, board, x, y, player):
        """检查落子是否合法（包括是否有气）"""
        if not board.is_valid_position(x, y):
            return False
        board.place_piece(x, y, player)
        if not self.has_liberty(board, x, y, player):
            board.move_piece(x, y, ".")  # 移除临时放置的棋子
            return False
        board.move_piece(x, y, ".")  # 移除临时放置的棋子
        return True