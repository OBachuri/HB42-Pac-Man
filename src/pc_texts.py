import pygame as pg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class PC_Texts():

    """Manages the temporary score text that appears and could float upward."""

    def __init__(self, game: "Game",
                 point: tuple[float, float] = (0, 0),
                 color: tuple[int, int, int] = (200, 250, 200),
                 text: str = 'event',
                 duration: float = 1,
                 fly: bool = False):

        self.game: "Game" = game
        self.x: float = 0
        self.y: float = 0
        self.x, self.y = point
        self.color: tuple[int, int, int] = color
        self.duration: float = duration  # in sec
        self.fly: bool = fly
        self.start_time = pg.time.get_ticks()
        self.surface = self.game.font.render(text, True, color)

    def update(self) -> None:
        """Moves text upward and checks if its lifetime has expired."""
        current_time = pg.time.get_ticks()
        elapsed = (current_time - self.start_time) / 1000

        # Float upward slowly
        if self.y > 0 and self.fly:
            self.y -= 0.05

        # Check if the text should be destroyed
        if elapsed >= self.duration:
            self.game.texts.remove(self)

    def draw(self) -> None:
        """Renders the text surface onto the screen."""
        x = self.x * self.game.map.step + self.game.screen_left_shift
        y = self.y * self.game.map.step + self.game.map.top
        self.game.screen.blit(self.surface, (x, y))
