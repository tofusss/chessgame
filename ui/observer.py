from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self):
        """响应被观察者的变化"""
        pass