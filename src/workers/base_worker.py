from abc import ABC, abstractmethod


class BaseWorker(ABC):
    @abstractmethod
    def run_until_complete(self) -> None:
        pass
