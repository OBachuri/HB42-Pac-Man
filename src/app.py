import asyncio
import pygame as pg
from src.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
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
        self.game = Game(self.config, self)
        self.current_score = 0

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
                    screen, InstructionsScreen(self.config, self))
            # case ScreenTypes.END_OF_GAME:
            #     if self.current_screen == ScreenTypes.GAME:
            #         self.current_score = self.game.score
            #     self.current_screen = self.screens.setdefault(
            #         screen, EndOfGameScreen(self))

    def quit(self) -> None:
        pg.quit()
        self.running = False

    def run(self) -> None:
        self.move_to(ScreenTypes.MAIN_MENU)
        while self.running:
            asyncio.run(self.current_screen.run())

            pg.display.flip()
            self.clock.tick(FPS)
