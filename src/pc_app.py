from __future__ import annotations
import sys
import os
import asyncio
import pygame as pg

from src.pc_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.pc_constants import MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT
from pc_game import Game
from pc_artifact import Pellet, Fruit
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
        try:
            pg.mixer.init()
            Game.sound_init()
            Pellet.sound_init()
            Fruit.sound_init()
        except Exception as ex:
            print("Error - no access to sound device:", ex)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption('Pac-man 42')

        self.fullscreen_mode: bool = False
        self.fullscreen_mode = self.config.fullscreen_mode

        self.running: bool = True

        self.screens: dict[ScreenTypes, BaseScreen] = {}
        self.current_screen: BaseScreen | None = None
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

    def move_to(self, screen: ScreenTypes) -> None:
        match screen:
            case ScreenTypes.MAIN_MENU:
                self.current_screen = self.screens.setdefault(
                    screen, MainMenuScreen(self))
            case ScreenTypes.GAME:
                self.game = Game(self)
                self.current_screen = self.game
            case ScreenTypes.INSTRUCTIONS:
                self.current_screen = self.screens.setdefault(
                    screen, InstructionsScreen(self))
            case ScreenTypes.HIGH_SCORES:
                self.score_to_show = -1
                if isinstance(self.current_screen, GameEndScreen):
                    self.score_to_show = self.game.score
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
        self.set_screen()

    def set_screen(self) -> None:
        if (not (self.current_screen is None)
           and self.current_screen.screen_type == ScreenTypes.GAME):
            if self.config.cheat:
                text_rows = 4 * self.game.map.top
            else:
                text_rows = 2 * self.game.map.top

            g_width = max(self.game.map.cols*self.game.map.step
                          + self.game.map.wall_thickness, SCREEN_WIDTH)
            g_height = max(self.game.map.rows * self.game.map.step + text_rows,
                           SCREEN_HEIGHT)

            if self.fullscreen_mode:
                if bool(self.screen.get_flags() & pg.FULLSCREEN):
                    size_ = self.screen.get_size()
                    if size_ == (g_width, g_height):
                        return
                pg.display.set_mode((g_width, g_height),
                                    pg.SCALED | pg.FULLSCREEN)
            else:
                # it not current display it is first
                current_screen_size = pg.display.get_desktop_sizes()[0]
                m_width, m_height = current_screen_size
                if ((m_width < g_width)
                   or (m_height < g_height)):
                    self.fullscreen_mode = True
                    pg.display.set_mode((g_width, g_height),
                                        pg.SCALED | pg.FULLSCREEN)
                else:
                    pg.display.set_mode((g_width, g_height))
        else:
            if self.fullscreen_mode:
                if bool(self.screen.get_flags() & pg.FULLSCREEN):
                    size_ = self.screen.get_size()
                    if size_ == (SCREEN_WIDTH, SCREEN_HEIGHT):
                        return
                pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                    pg.SCALED | pg.FULLSCREEN)
            else:
                # it not current display it is first
                current_screen_size = pg.display.get_desktop_sizes()[0]
                m_width, m_height = current_screen_size
                m_width = min(m_width - 10, SCREEN_WIDTH)
                m_height = min(m_height - 110, SCREEN_HEIGHT)
                if ((m_width < MIN_SCREEN_WIDTH)
                   or (m_height < MIN_SCREEN_HEIGHT)):
                    self.fullscreen_mode = True
                    pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                        pg.SCALED | pg.FULLSCREEN)
                else:
                    pg.display.set_mode((m_width, m_height))

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
