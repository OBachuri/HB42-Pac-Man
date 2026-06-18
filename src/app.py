from __future__ import annotations
import sys
import os
import asyncio
import pygame as pg

# relative_dir = os.path.dirname(__file__)
# os.path.join(os.path.dirname(__file__), '')
# print("=========", relative_dir)

# sys.path.append(os.path.dirname(__file__))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pc_game import Game
from screens import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .config import Config
    from .config_web import ConfigWeb


class App:
    def __init__(self, config: Config | ConfigWeb) -> None:
        self.config = config
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption('Pac-man 42')

        self.running = True
        self.screens: dict[ScreenTypes, BaseScreen] = {}
        self.current_screen = None
        self.path_to_inc = os.path.join(os.path.dirname(__file__), 'inc/')
        self.game = Game(self)

    def move_to(self, screen: ScreenTypes) -> None:
        match screen:
            case ScreenTypes.MAIN_MENU:
                self.current_screen = self.screens.setdefault(screen, MainMenuScreen(self))
            case ScreenTypes.GAME:
                # self.current_screen = self.screens.setdefault(screen, Game(self.config, self))
                self.current_screen = self.screens.setdefault(
                    screen, self.game)
            case ScreenTypes.INSTRUCTIONS:
                pass
                # self.current_screen = self.screens.setdefault(screen, InstructionsScreen(self.config, self))

    def quit(self) -> None:
        self.running = False
        if sys.platform != "emscripten":
            pg.quit()

    async def run(self) -> None:
        self.move_to(ScreenTypes.MAIN_MENU)
        while self.running:
            await self.current_screen.run()
            await asyncio.sleep(0)
            # pg.display.update()
            # self.clock.tick(FPS)
