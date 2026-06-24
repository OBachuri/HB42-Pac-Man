from __future__ import annotations
import sys
import os
import asyncio
import pygame as pg

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pc_game import Game
from screens import ScreenTypes, BaseScreen, MainMenuScreen, ErrorScreen
from screens import InstructionsScreen, HighscoresScreen, GameEndScreen
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config
    from config_web import ConfigWeb


class App:
    def __init__(self, config: Config | ConfigWeb) -> None:
        self.config = config
        self.err_msg: str = ""
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

        path_ = os.path.join(self.path_to_inc,
                             "fonts/PressStart2P-Regular.ttf")
        if os.path.exists(path_):
            self.large_font = pg.font.Font(path_, 30)
            self.small_font = pg.font.Font(path_, 20)
        else:
            print(f"The file with font does not exist: {path_} .")
            self.large_font = pg.font.SysFont('Nimbus Mono PS', 30)
            self.small_font = pg.font.SysFont('Nimbus Mono PS', 20)

        self.game = Game(self)

    def move_to(self, screen: ScreenTypes) -> None:
        match screen:
            case ScreenTypes.MAIN_MENU:
                self.current_screen = self.screens.setdefault(
                    screen, MainMenuScreen(self))
            case ScreenTypes.GAME:
                self.current_screen = self.screens.setdefault(
                    screen, self.game)
            case ScreenTypes.INSTRUCTIONS:
                self.current_screen = self.screens.setdefault(
                    screen, InstructionsScreen(self))
            case ScreenTypes.HIGH_SCORES:
                self.current_screen = self.screens.setdefault(
                    screen, HighscoresScreen(self))
            case ScreenTypes.END_OF_GAME:
                won = True if self.game.player.lives else False
                self.current_screen = GameEndScreen(self, won, self.game.score)
                self.game.level = 1
                self.game.next_level(0)
            case ScreenTypes.ERROR:
                self.current_screen = self.screens.setdefault(
                    screen, ErrorScreen(self))

    def quit(self) -> None:
        self.running = False
        if sys.platform != "emscripten":
            pg.quit()

    async def run(self) -> None:
        self.move_to(ScreenTypes.MAIN_MENU)
        while self.running:
            if self.current_screen:
                await self.current_screen.run()
            await asyncio.sleep(0)
