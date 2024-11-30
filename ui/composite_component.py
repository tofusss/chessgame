from ui.component import Component

class CompositeComponent(Component):
    """组合组件，管理多个子组件"""
    def __init__(self):
        super().__init__()
        self.children = []

    def add(self, component):
        """添加子组件"""
        self.children.append(component)

    def remove(self, component):
        """移除子组件"""
        self.children.remove(component)

    def display(self):
        """显示所有子组件"""
        if self.visible:
            for child in self.children:
                child.display()

    def toggle_visibility(self):
        """切换所有子组件的显示状态"""
        for child in self.children:
            child.toggle_visibility()