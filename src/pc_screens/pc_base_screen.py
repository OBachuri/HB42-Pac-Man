from abc import ABC, abstractmethod


class BaseScreen(ABC):
    @abstractmethod
    async def run(self) -> None:
        pass
