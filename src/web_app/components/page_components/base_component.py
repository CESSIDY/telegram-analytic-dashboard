from abc import ABC, abstractmethod


class BaseComponent(ABC):
    @abstractmethod
    def build(self):
        pass
