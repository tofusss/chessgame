import json

class FileManager:
    @staticmethod
    def save_to_file(file_path, data):
        """将数据保存到文件"""
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"局面已保存到文件：{file_path}")
        except Exception as e:
            print(f"保存失败：{e}")

    @staticmethod
    def load_from_file(file_path):
        """从文件加载数据"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            print(f"局面已从文件加载：{file_path}")
            return data
        except Exception as e:
            print(f"加载失败：{e}")
            return None