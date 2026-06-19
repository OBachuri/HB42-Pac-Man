import json
import asyncio
import pygame as pg
from screens import BaseScreen, ScreenTypes
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App


class HighscoresScreen(BaseScreen):
    def __init__(self, app: "App"):
        self.app = app
        self.highscores = self.read_highscores()

    def read_highscores(self) -> dict[str, int]:
        try:
            with open(self.app.config.highscores_filename) as f:
                return json.load(f)
        except Exception:
            return {}

    async def run(self) -> None:
        font = pg.font.SysFont("carlito", 30)
        title_font = pg.font.SysFont("carlito", 45)
        line_height = font.get_linesize() + 4
        title_line_height = title_font.get_linesize() + 4
        title_surf = title_font.render("Highscores:", None, "yellow")

        x = SCREEN_WIDTH // 2

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
            y = 10
            self.app.screen.blit(title_surf, (x - title_surf.width // 2, y))
            y += title_line_height

            if not self.highscores:
                score_surf = font.render(
                    "No results have been recorded so far.", None, "yellow")
                self.app.screen.blit(score_surf, (x - score_surf.width // 2, y))
            else:
                for highscore in self.highscores.items():
                    score_str = f"{highscore[0]}: {highscore[1]}"
                    score_surf = font.render(score_str, None, "yellow")
                    self.app.screen.blit(score_surf, (x - score_surf.width // 2, y))
                    y += line_height

            hint_surf = font.render("ESC: back", True, "white")
            self.app.screen.blit(hint_surf, (x - hint_surf.width // 2, SCREEN_HEIGHT - line_height))

            pg.display.flip()

            await asyncio.sleep(0)
