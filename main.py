from game.factory import GameFactory
from ui.console_ui import ConsoleUI
from player.player_factory import PlayerFactory
from player.account_manager import AccountManager

def get_board_size(game_type):
    """获取合法的棋盘大小"""
    while True:
        try:
            if game_type == "reversi":
                print("初始棋盘大小推荐为8*8")
            board_size = int(input("请输入棋盘大小（8-19）：").strip())
            if 8 <= board_size <= 19:
                return board_size
            else:
                print("输入的棋盘大小必须在 8 到 19 之间！")
        except ValueError:
            print("无效输入，请输入一个整数！")

def get_game_type():
    """获取合法的游戏类型"""
    valid_game_types = {"gomoku", "go","reversi"}  # 定义允许的游戏类型
    while True:
        game_type = input("请输入游戏类型（gomoku, go, reversi）：").strip().lower()
        if game_type in valid_game_types:
            return game_type
        elif game_type == 'q':  # 判断是否退出
            print("感谢使用，再见！")
            exit(0)
        else:
            print(f"无效的游戏类型！请从 {', '.join(valid_game_types)} 中选择。")

def select_ai_level():
    while True:
        try:
            ai_level = int(input("选择AI等级 1 or 2:").strip())
            if 1 <= ai_level <= 2:
                return ai_level
            else:
                print("1 or 2！")
        except ValueError:
            print("无效输入，请输入一个整数！")

def select_players(game_type):
    print("选择对战模式：1. 玩家-玩家 2. 玩家-AI 3. AI-AI")
    mode = input("请输入对战模式编号：").strip()

    player1 = None
    player2 = None

    if mode == "1":  # 玩家-玩家模式
        account_manager = AccountManager()
        print("玩家1请输入账户信息：")
        while not player1:
            try:
                username = input("用户名：")
                if username == "":
                    player1 = PlayerFactory.create_guest()
                else:
                    password = input("密码：")
                    account = account_manager.login(username, password)
                    player1 = PlayerFactory.create_registered(account)
            except ValueError as e:
                print(f"登录失败：{e}")
        
        print("玩家2请输入账户信息：")
        while not player2:
            try:
                username = input("用户名：")
                if username == "":
                    player1 = PlayerFactory.create_guest()
                else:
                    password = input("密码：")
                    account = account_manager.login(username, password)
                    player2 = PlayerFactory.create_registered(account)
            except ValueError as e:
                print(f"登录失败：{e}")
    
    elif mode == "2":  # 玩家-AI模式
        account_manager = AccountManager()
        print("玩家请输入账户信息：")
        while not player1:
            try:
                username = input("用户名：")
                if username == "":
                    player1 = PlayerFactory.create_guest()
                else:
                    password = input("密码：")
                    account = account_manager.login(username, password)
                    player1 = PlayerFactory.create_registered(account)
            except ValueError as e:
                print(f"登录失败：{e}")
        ai_level = 1
        if game_type == "gomoku":
            ai_level = select_ai_level()
        player2 = PlayerFactory.create_ai(ai_level)
    
    elif mode == "3":  # AI-AI模式
        ai_level = 1
        if game_type == "gomoku":
            ai_level = select_ai_level()
        player1 = PlayerFactory.create_ai(ai_level)
        player2 = PlayerFactory.create_ai(ai_level)
    
    else:
        print("无效的模式选择，请重试！")
        return None, None  # 返回空，主函数可重新处理选择

    return player1, player2

def main():
    try:
        while True:  # 使用循环让程序可以重复运行
            print("欢迎来到棋类对战平台！")
            print("支持的游戏类型：")
            print("1. gomoku - 五子棋")
            print("2. go - 围棋")
            print("3. reversi - 黑白棋")
            print("输入 'q' 关闭游戏")

            game_type = get_game_type()  # 调用合法输入检查函数
            board_size = get_board_size(game_type)  # 棋盘大小检查函数

            player1, player2 = select_players(game_type)
            if not player1 or not player2:
                continue  # 如果玩家未正确选择，则重新开始
            try:
                game = GameFactory.create_game(game_type, board_size)
                game.set_players(player1, player2)  # 假设 Game 支持设置玩家的方法
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
                break

    finally:
        # 程序退出前保存账户信息
        from player.account_manager import AccountManager
        print("正在保存账户信息...")
        AccountManager().save()
        print("保存成功！感谢使用，再见！")

if __name__ == "__main__":
    main()