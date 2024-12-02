class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    # def display(self):
    #     """打印当前棋盘状态"""
    #     print("   " + " ".join(f"{i:2}" for i in range(self.size)))
    #     for i, row in enumerate(self.grid):
    #         print(f"{i:2} " + " ".join(row))
    #     print()
    
    def display(self):
        """打印棋盘"""
        print("  " + " ".join(str(i) for i in range(self.size)))
        for y, row in enumerate(self.grid):
            print(str(y) + " " + " ".join(row))
        print()

    def place_piece(self, x, y, piece):
        """在棋盘上放置棋子"""
        if self.is_valid_position(x, y):
            self.grid[x][y] = piece
            return True
        return False
    
    def move_piece(self, x, y, piece):
        self.grid[x][y] = piece
        return True

    def is_valid_position(self, x, y):
        """判断位置是否合法"""
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == '.'
    
    def is_in_board(self, x, y):
        """判断位置是否合法"""
        return 0 <= x < self.size and 0 <= y < self.size

    def get_piece(self, x, y):
        """获取指定位置的棋子"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y]
        return None
    
    def is_board_full(self):
        """检查棋盘是否被占满"""
        for row in self.grid:
            if "." in row:  # 如果棋盘中还有空位，返回 False
                return False
        return True