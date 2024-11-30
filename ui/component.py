from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self):
        self.visible = True  # 控制显示状态

    @abstractmethod
    def display(self):
        """显示组件内容"""
        pass

    def toggle_visibility(self):
        """切换显示状态"""
        self.visible = not self.visible