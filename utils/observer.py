class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """添加观察者"""
        self._observers.append(observer)

    def notify_observers(self):
        """通知所有观察者"""
        for observer in self._observers:
            observer.update()