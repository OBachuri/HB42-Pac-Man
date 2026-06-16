import asyncio
import pygame as pg
from src.constants import *
from src.pc_game import Game
from src.config import Config
from src.screens import *


class App:
    def __init__(self, config: Config) -> None:
        self.config = config
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.screens: dict[ScreenTypes, BaseScreen] = {}
        self.current_screen = None

    def move_to(self, screen: ScreenTypes) -> None:
        match screen:
            case ScreenTypes.MAIN_MENU:
                self.current_screen = self.screens.setdefault(screen, MainMenuScreen(self))
            case ScreenTypes.GAME:
                self.current_screen = self.screens.setdefault(screen, Game(self.config, self))
            case ScreenTypes.INSTRUCTIONS:
                self.current_screen = self.screens.setdefault(screen, InstructionsScreen(self.config, self))

    def quit(self) -> None:
        pg.quit()
        self.running = False

    def run(self) -> None:
        self.move_to(ScreenTypes.MAIN_MENU)
        while self.running:
            asyncio.run(self.current_screen.run())

            pg.display.update()
            self.clock.tick(FPS)
