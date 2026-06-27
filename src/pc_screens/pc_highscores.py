import asyncio
import pygame as pg
from pc_highscore_handler import HighscoresHandler
from pc_screens import BaseScreen, ScreenTypes
from pc_constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_app import App


class HighscoresScreen(BaseScreen):
    def __init__(self, app: "App"):
        self.app = app

    async def run(self) -> None:
        highscores = HighscoresHandler.get_highscores(self.app.config)

        place_info = ""
        if self.app.score_to_show >= 0:
            score_vals = [list(d.values())[0] for d in highscores]
            try:
                place = score_vals.index(self.app.score_to_show, 0) + 1
            except ValueError:
                place = 11
            if place > 10:
                place_info = "Sorry, you are not in top 10"
            else:
                place_info = f"You are in {place} place"

        font = self.app.small_font
        title_font = self.app.large_font
        line_height = font.get_linesize() + 8
        title_line_height = title_font.get_linesize() + 8
        title_surf = title_font.render("Highscores:", False, "yellow")

        place_inf_surf = font.render(place_info, False, "white")

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
            y = 60
            self.app.screen.blit(title_surf, (x - title_surf.width // 2, y))
            y += title_line_height * 2

            if not highscores:
                score_surf = font.render(
                    "No results have been recorded so far.", False, "yellow")
                self.app.screen.blit(score_surf,
                                     (x - score_surf.width // 2, y))
            else:
                if place_info:
                    self.app.screen.blit(place_inf_surf,
                                         (x - place_inf_surf.width // 2, y))
                    y += line_height * 1.5
                for nbr, highscore in enumerate(highscores, start=1):
                    name, score = list(highscore.items())[0]
                    score_str = f"{nbr}. {name} - {score}"
                    score_surf = font.render(score_str, False, "yellow")
                    self.app.screen.blit(score_surf,
                                         (x - score_surf.width // 2, y))
                    y += line_height * 1.5

            hint_surf = font.render("ESC: back", True, "white")
            self.app.screen.blit(hint_surf, (x - hint_surf.width // 2,
                                             SCREEN_HEIGHT - line_height))

            pg.display.flip()

            await asyncio.sleep(0)
