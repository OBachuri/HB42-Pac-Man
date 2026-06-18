import asyncio
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App

from constants import SCREEN_WIDTH  # , SCREEN_HEIGHT
from screens import BaseScreen, ScreenTypes


class Button:
    def __init__(
            self,
            y: int,
            width: int,
            text: str,
            icon: pg.Surface,
            x: int = SCREEN_WIDTH // 2 - 75,
            height: int = 50) -> None:
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.hovered = False
        self.selected = False

    def draw(self, surface) -> None:
        # Draw button border
        pg.draw.rect(surface, "yellow", self.rect, 2)

        # Draw image on the left if selected
        if self.selected or self.hovered:
            img_rect = self.icon.get_rect(
                center=(self.rect.left - 40, self.rect.centery))
            surface.blit(self.icon, img_rect)

        # Draw text
        text_surf = pg.font.Font(None, 30).render(self.text, True, "yellow")
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos) -> bool:
        return self.rect.collidepoint(pos)

    def update(self, pos) -> None:
        self.hovered = self.rect.collidepoint(pos)


class MainMenuScreen(BaseScreen):
    def __init__(self, app: "App"):
        # from app import App
        self.app = app

    async def run(self) -> None:
        screen = self.app.screen
        pg.display.set_caption("Pac-Man")
        clock = pg.time.Clock()
        pacman_icon = pg.image.load(
            self.app.path_to_inc + "img/pacman/stay/S01.png").convert_alpha()

        buttons = [
            Button(y=200, width=150, text="START GAME", icon=pacman_icon),
            Button(y=300, width=220, text="VIEW HIGHSCORES", icon=pacman_icon),
            Button(y=400, width=200, text="INSTRUCTIONS", icon=pacman_icon),
            Button(y=500, width=150, text="EXIT", icon=pacman_icon)
        ]

        selected_index = 0
        buttons[selected_index].selected = True

        running = True
        while running:
            clock.tick(60)
            mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.app.quit()

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
                            print("Opening highscores...")
                        elif selected_button.text == "INSTRUCTIONS":
                            self.app.move_to(ScreenTypes.INSTRUCTIONS)
                            running = False
                        elif selected_button.text == "EXIT":
                            self.app.quit()

                    elif event.key == pg.K_ESCAPE:
                        self.app.quit()

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
                                print("Opening highscores...")
                            elif button.text == "INSTRUCTIONS":
                                self.app.move_to(ScreenTypes.INSTRUCTIONS)
                                running = False
                            elif button.text == "EXIT":
                                self.app.quit()

            for i, button in enumerate(buttons):
                button.update(mouse_pos)
                if button.hovered:
                    buttons[selected_index].selected = False
                    selected_index = i
                    buttons[selected_index].selected = True

            screen.fill("black")
            title = pg.font.Font(None, 80).render("PAC-MAN", True, "yellow")
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title, title_rect)

            for button in buttons:
                button.draw(screen)

            pg.display.flip()

            await asyncio.sleep(0)
