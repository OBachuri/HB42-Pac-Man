from abc import ABC, abstractmethod
from pc_screens import ScreenTypes


class BaseScreen(ABC):
    """Abstract base class for all application screens.

    Defines the common screen contract used by the app's async loop.
    """

    screen_type: ScreenTypes = ScreenTypes.ERROR

    @abstractmethod
    async def run(self) -> None:
        """Execute one asynchronous screen loop until transition/exit."""
        pass
