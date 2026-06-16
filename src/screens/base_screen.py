from abc import ABC, abstractmethod


class BaseScreen(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
