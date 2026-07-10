from __future__ import annotations

import pygame as pg
from enum import Enum
import os

from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class FrameType(Enum):
    """Animation frame states for player and ghost sprite sequences."""

    # stay / run / left / right / top / bottom / dead / frightened
    STAY = 1
    RUN = 2
    LEFT = 3
    RIGHT = 4
    UP = 5
    DOWN = 6
    DEATH = 7
    DEAD = 8
    FRIGHTENED = 9
    END_OF_FRIGHTENED = 10


class GhostMode(Enum):
    """Behavior modes that control ghost AI movement and targeting."""

    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3
    STROLL = 4
    DEAD = 9
    SPAWN = 10
    FREEZE = 99


class Entity:
    """Base movable entity for player and ghosts.

    Provides shared state and behavior for position, movement, animation,
    collision checks, teleporting, and sprite frame loading.
    """

    def __init__(self,
                 game: Game,
                 point: tuple[float, float] = (0, 0),
                 color: tuple[int, int, int] = (50, 50, 50),
                 name: str = "Entity",
                 size: int = 11):
        """Initialize common entity properties.

        Args:
            game (Game): Active game context.
            point (tuple[float, float], optional): Initial map position.
            color (tuple[int, int, int], optional): Default render color.
            name (str, optional): Entity display/debug name.
            size (int, optional): Collision/render size factor.
        """

        self.game = game
        self.x: float = 0
        self.y: float = 0
        self.x, self.y = point
        self.start_x, self.start_y = point
        self.name = name
        self.size = size  # radius
        self.alive: bool = True
        self.freeze: bool = False
        self.invincibil: bool = False
        self.dx: int = 0
        self.dy: int = 0
        self.color = color  # (R,G,B)
        self.frames: dict[FrameType, list[pg.Surface]] = {}
        self.mode: GhostMode = GhostMode.STROLL
        self.frame_index: int = 0
        self.animation_timer: float = 0
        self.event_timer: float = 0
        self.speed_factor: float = 0.04
        self.visible: bool = True
        self.max_d: int = 5  # max dx + dy = maximum acceleration
        self.sounds: dict[SoundType, list[Sound]] = {}
        self.sound_index: int = 0

    def reset(self) -> None:
        """Reset movement, animation, and lifecycle state to spawn defaults."""

        self.dx = 0
        self.dy = 0
        self.teleport()
        self.frame_index = 0
        self.animation_timer = 0
        self.alive = True
        self.visible = True

    def teleport(self, x: int = -1, y: int = -1) -> None:
        """Move entity instantly to coordinates or starting position.

        Args:
            x (int, optional): Target x coordinate, or start x if negative.
            y (int, optional): Target y coordinate, or start y if negative.
        """

        if x < 0:
            x = int(self.start_x)
        if y < 0:
            y = int(self.start_y)
        self.x = int(x)
        self.y = int(y)

    def movement(self) -> None:
        """Update entity movement for the current frame."""
        pass

    def update(self) -> None:
        """Advance movement and animation state for one tick."""

        self.movement()
        if self.alive:
            self.animation_timer += 0.1
            + (abs(self.dx) + abs(self.dy)) * self.speed_factor*5
        else:
            self.animation_timer += 0.1
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1

    def collide_check(self, o_: "Entity") -> bool:
        """Check circular proximity collision against another entity.

        Args:
            o_ (Entity): Other entity to test collision with.

        Returns:
            bool: True if entities overlap within collision threshold.
        """

        x = o_.x
        y = o_.y
        s = o_.size
        # print("o(x,y,s)",x,y,s,f"{o_.name}^{self.name}",
        # " c(x,y,s)", self.x,self.y,self.size)
        # print(((self.x - x)**2 + (self.y - y)**2))
        # print(((self.size + s)/self.game.map.step)**2)
        # return ((((self.x - x)**2
        #         + (self.y - y)**2)
        #         < ((self.size + s)/self.game.map.step)**2))
        if (((self.x - x)**2 + (self.y - y)**2)
                < ((self.size + s)/self.game.map.step)**2):
            return (True)
        return (False)

    def draw(self) -> None:
        """Render entity on the game surface."""

        if not (self.visible):
            return

        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.screen_left_shift)

        y = (self.y * (self.game.map.step)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        frames = []

        if not (self.alive):
            if (((self.mode == GhostMode.FRIGHTENED)
                 or (self.mode == GhostMode.DEAD))):
                frames = self.frames.get(FrameType.DEATH, [])
                # print("DEATH from", len(frames), self.frame_index)
            elif (self.mode == GhostMode.SPAWN):
                if self.dy < 0:  # up / to top
                    frames = self.frames.get(FrameType.UP, [])
                elif self.dy > 0:  # down / to bottom
                    frames = self.frames.get(FrameType.DOWN, [])
                elif self.dx < 0:  # left
                    frames = self.frames.get(FrameType.LEFT, [])
                elif self.dx > 0:  # right
                    frames = self.frames.get(FrameType.RIGHT, [])
                else:
                    frames = self.frames.get(FrameType.DEAD, [])
        elif (self.mode == GhostMode.FRIGHTENED):
            if self.event_timer > 2:
                frames = self.frames.get(FrameType.FRIGHTENED, [])
            else:
                frames = self.frames.get(FrameType.END_OF_FRIGHTENED, [])
        elif (self.dx == 0) and (self.dy == 0):
            frames = self.frames.get(FrameType.STAY, [])
        else:
            frames = self.frames.get(FrameType.RUN, [])
        if len(frames) > 0:
            if self.frame_index >= len(frames):
                if (not (self.alive)) and (self.mode != GhostMode.SPAWN):
                    self.frame_index = len(frames) - 1
                    self.after_death()
                    return
                self.frame_index = 0
            image = frames[self.frame_index]
            rect = image.get_rect(center=(int(x), int(y)))
            self.game.screen.blit(image, rect)
        else:
            pg.draw.circle(self.game.screen,
                           self.color,
                           (x, y), self.size)

    def after_death(self) -> None:
        """Apply post-death behavior for the entity."""
        pass

    def read_frames_from_file(
            self, file_path: str, frame_type: FrameType) -> None:
        """Load animation frames for a given frame type from disk.

        Args:
            file_path (str): Directory or base path containing frame images.
            frame_type (FrameType): Target animation category to populate.
        """

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
