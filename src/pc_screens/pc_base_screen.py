from abc import ABC, abstractmethod
<<<<<<< HEAD:src/pc_screens/pc_base_screen.py
from pc_screens import ScreenTypes
=======
from screens import ScreenTypes
>>>>>>> main:src/screens/base_screen.py


class BaseScreen(ABC):
    screen_type: ScreenTypes = ScreenTypes.ERROR

    @abstractmethod
    async def run(self) -> None:
        pass
