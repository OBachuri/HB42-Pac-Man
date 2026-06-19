import json
import asyncio
import pygame as pg
from screens import BaseScreen, ScreenTypes
from constants import FPS
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App


class HighscoresScreen(BaseScreen):
    def __init__(self, app: "App"):
        self.app = app

    async def run(self) -> None:
        font = pg.font.SysFont("carlito", 30)

        running = True
        while running:
            self.app.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                        self.app.move_to(ScreenTypes.MAIN_MENU)

            self.app.screen.fill("black")

            pg.display.flip()

            await asyncio.sleep(0)
