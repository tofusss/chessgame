from game.factory import GameFactory
def get_board_size():
    """获取合法的棋盘大小"""
    while True:
        try:
            board_size = int(input("请输入棋盘大小（8-19）：").strip())
            if 8 <= board_size <= 19:
                return board_size
            else:
                print("输入的棋盘大小必须在 8 到 19 之间！")
        except ValueError:
            print("无效输入，请输入一个整数！")

def get_game_type():
    """获取合法的游戏类型"""
    valid_game_types = {"gomoku", "go"}  # 定义允许的游戏类型
    while True:
        game_type = input("请输入游戏类型（gomoku, go）：").strip().lower()
        if game_type in valid_game_types:
            return game_type
        elif game_type == 'q':  # 判断是否退出
            print("感谢使用，再见！")
            exit(0)
        else:
            print(f"无效的游戏类型！请从 {', '.join(valid_game_types)} 中选择。")

def main():
    while True:  # 使用循环让程序可以重复运行
        print("欢迎来到棋类对战平台！")
        print("支持的游戏类型：")
        print("1. gomoku - 五子棋")
        print("2. go - 围棋")
        print("输入 'q' 关闭游戏")

        game_type = get_game_type()  # 调用合法输入检查函数
        board_size = get_board_size()  # 之前已实现的棋盘大小检查函数

        try:
            game = GameFactory.create_game(game_type, board_size)
            from ui.console_ui import ConsoleUI
            ui = ConsoleUI(game, game_type)
            ui.run()  # 启动用户交互
        except ValueError as e:
            print(f"错误：{e}")
        except Exception as e:
            print(f"未知错误：{e}")

        # 在这里可以询问用户是否继续
        print("\n是否要重新开始？输入 'y' 继续，或其他任意键退出")
        restart = input().strip().lower()
        if restart != 'y':
            print("感谢使用，再见！")
            break

if __name__ == "__main__":
    main()