import pygame as pg
from pc_entity import FrameType, GhostMode
from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.pc_game import Game


class PC_Artifacts():
    """
    Artifacts = Pellet or PowerPellet

    Pellet = Dot = Pacgums
    PowerPellet = Super-pacgums = Energizer
    """

    frames: dict[FrameType, list[pg.Surface]] = {}
    frame_index: int = 0
    sounds: dict[SoundType, list[Sound]] = {}
    sound_index: int = 0

    def __init__(self, game: "Game",
                 point: tuple[int | float, int | float] = (0, 0),
                 points: int = 10,
                 color: tuple[int, int, int] = (200, 200, 200)):
        self.game = game
        self.x, self.y = point
        self.size: int = 2  # radius
        self.color = color
        self.points = points  # score add

    def draw(self) -> None:
        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.screen_left_shift)

        y = (self.y * (self.game.map.step)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        if len(self.frames) == 0:
            pg.draw.circle(self.game.screen,
                           self.color,
                           (x, y), self.size)

    def event(self) -> None:
        self.game.score += self.points
        self.points = 0
        self.color = (255, 255, 255)
        self.draw()
        # self.game.player.dx = max(0, self.game.player.dx - 0.1)
        # self.game.player.dy = max(0, self.game.player.dy - 0.1)
        self.game.artifacts.remove(self)

    def update(self) -> None:
        x = int(round(self.game.player.x, 0))
        y = int(round(self.game.player.y, 0))
        if (x, y) == (self.x, self.y):
            if ((self.x - self.game.player.x)**2
                + (self.y
                   - self.game.player.y)**2) < (self.size
                                                + self.game.player.size)**2:
                self.event()


class PowerPellet(PC_Artifacts):
    # PowerPellet = Super-pacgums = Energizer
    def __init__(self, game: "Game",
                 point: tuple[int | float, int | float] = (0, 0),
                 points: int = 50,
                 color: tuple[int, int, int] = (220, 250, 220)) -> None:
        super().__init__(game, point, points, color)
        self.size: int = 6  # radius

    def event(self) -> None:
        super().event()
        self.game.player.dx = max(0, self.game.player.dx - 3)
        self.game.player.dy = max(0, self.game.player.dy - 3)
        for n in self.game.npcs:
            if n.alive:
                n.mode = GhostMode.FRIGHTENED
                n.dx *= -1
                n.dy *= -1
                n.event_timer = self.game.gost_edible

        sound = self.sounds.get(SoundType.EATEN, [])
        if len(sound) > 0:
            if self.sound_index >= len(sound):
                type(self).sound_index = 0
            sound[type(self).sound_index].play()
            type(self).sound_index += 1


class Pellet(PC_Artifacts):
    # Pellet = Pacgums = Dots

    @classmethod
    def sound_init(cls) -> None:
        cls.sounds = Sound.read_sounds_from_files(
            "inc/sounds/pacgum/", SoundType.EATEN)

    def __init__(self, game: "Game",
                 point: tuple[int | float, int | float] = (0, 0),
                 points: int = 10,
                 color: tuple[int, int, int] = (220, 220, 250)) -> None:
        super().__init__(game, point, points, color)

    def event(self) -> None:
        sound = self.sounds.get(SoundType.EATEN, [])
        if len(sound) > 0:
            if self.sound_index >= len(sound):
                type(self).sound_index = 0
            sound[type(self).sound_index].play()
            type(self).sound_index += 1

        super().event()


class Fruit(PC_Artifacts):
    def __init__(self, game: "Game",
                 point: tuple[int | float, int | float] = (0, 0),
                 points: int = 100,
                 color: tuple[int, int, int] = (120, 250, 120)) -> None:
        super().__init__(game, point, points, color)
        self.size: int = 15     # radius
        self.event_timer = 9    # s - time of live
