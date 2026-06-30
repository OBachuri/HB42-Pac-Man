from abc import ABC, abstractmethod
from screens import ScreenTypes


class BaseScreen(ABC):
    screen_type: ScreenTypes = ScreenTypes.ERROR

    @abstractmethod
    async def run(self) -> None:
        pass
