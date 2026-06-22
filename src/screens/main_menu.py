import sys
import asyncio
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App

from constants import SCREEN_WIDTH, FPS
from screens import BaseScreen, ScreenTypes
from screens.utils import Button


class MainMenuScreen(BaseScreen):
    def __init__(self, app: "App"):
        self.app = app
        self.pacman_icon = pg.image.load(
            self.app.path_to_inc + "img/pacman/stay/S01.png").convert_alpha()

    async def run(self) -> None:
        pg.display.set_caption("Pac-Man")
        clock = self.app.clock

        buttons = [
            Button(y=200, text="START GAME",
                   icon=self.pacman_icon, font=self.app.small_font),
            Button(y=300, text="VIEW HIGHSCORES",
                   icon=self.pacman_icon, font=self.app.small_font),
            Button(y=400, text="INSTRUCTIONS",
                   icon=self.pacman_icon, font=self.app.small_font)
        ]
        if sys.platform != "emscripten":
            buttons.append(Button(y=500, width=150, text="EXIT",
                                  icon=self.pacman_icon, font=self.app.small_font))

        selected_index = 0
        buttons[selected_index].selected = True

        title = self.app.large_font.render("PAC-MAN", True, "yellow")
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))

        running = True
        while running:
            clock.tick(FPS)
            mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.app.quit()
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        buttons[selected_index].selected = False
                        selected_index = (selected_index - 1) % len(buttons)
                        buttons[selected_index].selected = True

                    elif event.key == pg.K_DOWN:
                        buttons[selected_index].selected = False
                        selected_index = (selected_index + 1) % len(buttons)
                        buttons[selected_index].selected = True

                    elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        selected_button = buttons[selected_index]
                        if selected_button.text == "START GAME":
                            self.app.move_to(ScreenTypes.GAME)
                            running = False
                        elif selected_button.text == "VIEW HIGHSCORES":
                            self.app.move_to(ScreenTypes.HIGH_SCORES)
                            running = False
                        elif selected_button.text == "INSTRUCTIONS":
                            self.app.move_to(ScreenTypes.INSTRUCTIONS)
                            running = False
                        elif selected_button.text == "EXIT":
                            self.app.quit()
                            running = False

                    elif (event.key == pg.K_ESCAPE and
                          sys.platform != "emscripten"):
                        self.app.quit()
                        running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if button.is_clicked(mouse_pos):
                            buttons[selected_index].selected = False
                            selected_index = i
                            buttons[selected_index].selected = True

                            # Trigger button action
                            if button.text == "START GAME":
                                self.app.move_to(ScreenTypes.GAME)
                                running = False
                            elif button.text == "VIEW HIGHSCORES":
                                self.app.move_to(ScreenTypes.HIGH_SCORES)
                                running = False
                            elif button.text == "INSTRUCTIONS":
                                self.app.move_to(ScreenTypes.INSTRUCTIONS)
                                running = False
                            elif button.text == "EXIT":
                                self.app.quit()
                                running = False

            for i, button in enumerate(buttons):
                button.update(mouse_pos)
                if button.hovered:
                    buttons[selected_index].selected = False
                    selected_index = i
                    buttons[selected_index].selected = True

            if running:
                self.app.screen.fill("black")
                self.app.screen.blit(title, title_rect)

                for button in buttons:
                    button.draw(self.app.screen)

                pg.display.flip()

            await asyncio.sleep(0)
