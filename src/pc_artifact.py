import os
import pygame as pg
from enum import Enum
import random


from pc_entity import FrameType, GhostMode
from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.pc_game import Game


class BonusFruitType(Enum):
    """
    Clasic bonus/fruits:
    Level / Name / Points
    1 Cherry 100
    2 Strawberry 300
    3-4 Orange 500
    5-6 Apple 700
    7-8 Melon 1000
    9-10 Galaxian 2000
    11-12 Bell 3000
    13+ Key 5000
    """

    CHERRY = 100
    RASPBERRY = 200
    STRAWBERRY = 300
    ORANGE = 500
    APPLE = 700
    BANANA = 800
    MELON = 1000
    BELL = 3000
    KEY = 5000


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
                 point: tuple[int, int] = (0, 0),
                 points: int = 10,
                 color: tuple[int, int, int] = (200, 200, 200),
                 name: str = 'Artifact'):
        self.game = game
        self.x, self.y = point
        self.size: int = 2  # radius
        self.color = color
        self.points = points  # score add
        self.name = name
        self.event_timer: float = 0

    def draw(self) -> None:
        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.screen_left_shift)

        y = (self.y * (self.game.map.step)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        # frames = []
        frames = self.frames.get(FrameType.STAY, [])

        if len(frames) > 0:
            if self.frame_index >= len(frames):
                self.frame_index = 0
            image = frames[self.frame_index]
            rect = image.get_rect(center=(int(x), int(y)))
            self.game.screen.blit(image, rect)
        else:
            pg.draw.circle(self.game.screen,
                           self.color,
                           (x, y), self.size)

    def event(self) -> None:
        self.game.score += self.points
        self.points = 0
        self.color = (255, 255, 255)
        self.draw()

        sound = self.sounds.get(SoundType.EATEN, [])
        if len(sound) > 0:
            if self.sound_index >= len(sound):
                type(self).sound_index = 0
            sound[type(self).sound_index].play()
            type(self).sound_index += 1

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
                 point: tuple[int, int] = (0, 0),
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


class Pellet(PC_Artifacts):
    # Pellet = Pacgums = Dots

    @classmethod
    def sound_init(cls) -> None:
        cls.sounds = Sound.read_sounds_from_files(
            "inc/sounds/pacgum/", SoundType.EATEN)

    def __init__(self, game: "Game",
                 point: tuple[int, int] = (0, 0),
                 points: int = 10,
                 color: tuple[int, int, int] = (220, 220, 250)) -> None:
        super().__init__(game, point, points, color)

    def event(self) -> None:
        if len(self.game.fruits_triger) > 0:
            if len(self.game.artifacts) < self.game.fruits_triger[0]:
                bonus_fruit = Fruit(self.game, type=self.game.bonus_fruit_type)
                bonus_fruit.teleport()
                self.game.artifacts.append(bonus_fruit)
                del self.game.fruits_triger[0]
                for n in self.game.npcs:
                    if n.alive and (n.mode != GhostMode.FRIGHTENED):
                        n.mode = GhostMode.CHASE
        super().event()


class Fruit(PC_Artifacts):
    def __init__(self, game: "Game",
                 point: tuple[int, int] = (0, 0),
                 points: int = 100,
                 color: tuple[int, int, int] = (120, 250, 120),
                 name: str = "Fruit",
                 type: BonusFruitType = BonusFruitType.CHERRY) -> None:
        super().__init__(game, point, points, color, name=name)
        self.size: int = 15     # radius
        self.event_timer = 9    # s - time of live
        self.frames: dict[FrameType, list[pg.Surface]] = {}
        self.frame_index: int = 0
        self.animation_timer: float = 0
        self.type: BonusFruitType = type
        self.event_timer: float = 9  # sec - disappears after 9 sec.

        f_name: str = str(self.type.name).lower()
        self.read_frames_from_file(
            "inc/img/artifacts/" + f_name + "/", FrameType.STAY)

    def teleport(self, x: int | float = -1, y: int | float = -1) -> None:
        if (x > 0) and (y > 0):
            self.x = int(x)
            self.y = int(y)
            return
        # A random place but not near PacMan
        min_dis = 1
        if self.game.map.cols > 10 and self.game.map.rows > 10:
            min_dis = 5
        elif self.game.map.cols > 6 and self.game.map.rows > 6:
            min_dis = 3
        place_set = {
            (x, y) for x in range(0, self.game.map.cols)
            for y in range(0, self.game.map.rows)
            if ((self.game.map.world_map.get((x, y), 0) & 15 != 15)
                and abs(x-self.game.player.x) > min_dis
                and abs(y-self.game.player.y) > min_dis
                )}
        if len(place_set) < 2:
            place_set = {
                (x, y) for x in range(0, self.game.map.cols)
                for y in range(0, self.game.map.rows)
                if (self.game.map.world_map.get((x, y), 0) & 15 != 15)}
            place_set.remove((int(self.game.player.x),
                              int(self.game.player.y)))

        x, y = random.choice(tuple(place_set))
        self.x = int(x)
        self.y = int(y)

    def read_frames_from_file(
            self, file_path: str, frame_type: FrameType) -> None:

        path_ = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                file_path,
            )
        if os.path.exists(path_):
            files = sorted(
                f for f in os.listdir(path_)
                if f.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".webp")
                )
            )
            if len(self.frames.get(frame_type, [])) == 0:
                self.frames[frame_type] = []

            for filename in files:
                frame = pg.image.load(
                    os.path.join(path_, filename)
                ).convert_alpha()
                self.frames[frame_type].append(frame)
            #     print(filename)
            # print(self.frames[frame_type])

            if not self.frames[frame_type]:
                print(f"No image files found in {path_}.")
        else:
            print(f"Can't find images files in {file_path}"
                  f"for {frame_type.name} of {self.name}.")

    def event_end(self) -> None:
        # print("Fr End:", self.event_timer, self.name)
        self.points = 0
        self.color = (255, 255, 255)
        self.draw()

        sound = self.sounds.get(SoundType.DISAPPEAR, [])
        if len(sound) > 0:
            sound[0].play()
        self.game.artifacts.remove(self)
        if len(self.game.artifacts) > 10:
            for n in self.game.npcs:
                if n.alive and (n.mode != GhostMode.FRIGHTENED):
                    n.mode = GhostMode.STROLL

    def update(self) -> None:
        self.animation_timer += 0.1
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1
        if self.event_timer > 0:
            self.event_timer -= 1 / self.game.fps
            if self.event_timer <= 0:
                self.event_timer = 0
                self.event_end()

        super().update()

    @classmethod
    def sound_init(cls) -> None:
        cls.sounds = Sound.read_sounds_from_files(
            "inc/sounds/bonusfruit/eaten/", SoundType.EATEN)
