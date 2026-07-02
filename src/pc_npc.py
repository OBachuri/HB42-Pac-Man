from __future__ import annotations

import pygame as pg
import random
from collections.abc import Sequence
# from enum import Enum
from pc_entity import Entity, FrameType, GhostMode
from pc_constants import FPS
from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class NPC(Entity):
    """ Ghosts """

    def __init__(self, game: Game,
                 point: tuple[int | float, int | float] = (0, 0),
                 color: tuple[int, int, int] = (100, 100, 100),
                 name: str = "Ghost", size: int = 11, points: int = 200):
        super().__init__(game, point=point, color=color, name=name, size=size)
        self.speed_factor: float = 0.02
        self.points = points  # score add

        # for mypy test - it can't check type from Entity
        self.dx: int = 0
        self.dy: int = 0

        self.goal: pg.Vector2 | None = None
        self.x: float | int = 0
        self.y: float | int = 0
        self.x, self.y = point
        self.angle: float | int = 0
        self.animation_timer: float = 0
        self.event_timer: float = 0
        self.sounds: dict[SoundType, list[Sound]] = {}
        self.sound_index: int = 0
        # end of block for mypy

        self.start_chase_if_near: int = 4
        self.mode: GhostMode = GhostMode.CHASE

        self.read_frames_from_file("inc/img/frightened/", FrameType.FRIGHTENED)
        self.read_frames_from_file("inc/img/end_of_frightened/",
                                   FrameType.END_OF_FRIGHTENED)
        self.read_frames_from_file("inc/img/ghost/death/", FrameType.DEATH)
        self.read_frames_from_file("inc/img/ghost/eyes/down/", FrameType.DOWN)
        self.read_frames_from_file("inc/img/ghost/eyes/up/", FrameType.UP)
        self.read_frames_from_file("inc/img/ghost/eyes/left/", FrameType.LEFT)
        self.read_frames_from_file("inc/img/ghost/eyes/right/",
                                   FrameType.RIGHT)
        self.alive: bool = True
        self.visible: bool = True
        self.freeze: bool = False

        self.old_keys: Sequence[bool] = pg.key.get_pressed()

        self.sound_init()

    def find_goal(self) -> None:
        if (
            self.mode == GhostMode.SCATTER
            and (self.goal is None
                 or tuple(self.goal) != (self.start_x, self.start_y))
        ):
            self.goal = pg.Vector2(self.start_x, self.start_y)
        else:
            if ((self.goal is None)
               or self.goal == (round(self.x), round(self.y))):
                # We have reached the goal and we need a new one
                if self.mode == GhostMode.SCATTER and self.game.chase_phase:
                    self.mode = GhostMode.CHASE
                    return
                x_g = random.randrange(0, self.game.map.cols)
                y_g = random.randrange(0, self.game.map.rows)
                i = 20
                while (self.game.map.world_map.get((x_g, y_g), 0)
                        & 0xf == 0xf and i > 0):
                    x_g = random.randrange(0, self.game.map.cols)
                    y_g = random.randrange(0, self.game.map.rows)
                    i -= 1
                if i > 0:
                    self.goal = pg.Vector2(x_g, y_g)

    def movement(self) -> None:

        keys = pg.key.get_pressed()

        if self.old_keys != keys:
            self.old_keys = keys
            if self.game.config.cheat:
                if keys[pg.K_f]:
                    self.mode = GhostMode.SCATTER
                if keys[pg.K_7]:
                    if self.mode == GhostMode.SCATTER:
                        self.mode = GhostMode.STROLL
                    elif self.mode == GhostMode.STROLL:
                        self.mode = GhostMode.CHASE
                    else:
                        self.mode = GhostMode.SCATTER
                if keys[pg.K_3]:
                    self.freeze = not (self.freeze)

        x: float = float(self.x)
        y: float = float(self.y)

        if self.freeze:
            if self.mode == GhostMode.SPAWN:
                if (not (self.goal is None)
                   and tuple(self.goal) == (x, y)):
                    self.reborn()
            return

        if self.mode == GhostMode.SPAWN:
            speed_factor = max(0.05, self.speed_factor)
        else:
            speed_factor = self.speed_factor

        if (((abs(round(x) - x) < speed_factor)
             and (abs(round(y) - y) < speed_factor))):
            x = round(x)
            y = round(y)

            if self.mode == GhostMode.SPAWN:
                if self.goal == pg.Vector2(x, y):
                    self.reborn()
            else:
                self.find_goal()

            # Check if player near and not ghosts etable now

            if self.goal is None:
                return
            P_ = self.game.map.find_path((x, y), tuple(self.goal))
            # print("ghost", self.name, "path:", P_)
            if len(P_) > 1:
                dx = P_[1][0] - x
                dx = int(dx > 0) - int(dx < 0)
                dy = P_[1][1] - y
                dy = int(dy > 0) - int(dy < 0)
                self.dx = dx
                self.dy = dy
            else:
                dx = 0
                dy = 0
        else:
            dx = self.dx
            dy = self.dy

        x = speed_factor * dx + self.x
        y = speed_factor * dy + self.y

        self.x = x
        self.y = y

    def update(self) -> None:
        if self.event_timer > 0:
            self.event_timer -= 1/FPS
            if self.event_timer <= 0:
                self.event_timer = 0
                self.event_end()
        self.movement()
        self.animation_timer += 0.1
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1
        if self.visible and self.collide_check(self.game.player):
            self.event()

    def event_end(self) -> None:
        # print("Fr End:", self.event_timer, self.mode, self.name)
        if self.mode == GhostMode.FRIGHTENED:
            if self.game.chase_phase:
                self.mode = GhostMode.CHASE
            else:
                self.mode = GhostMode.SCATTER

    def event(self) -> None:
        if not self.alive:
            return
        print("Collide PacMan and", self.name, "!")
        if self.mode == GhostMode.FRIGHTENED:
            self.game.score += self.points
            self.mode = GhostMode.DEAD
            self.alive = False
            sound = self.sounds.get(SoundType.EATEN, [])
            if len(sound) > 0:
                sound[0].play()

        else:
            if self.game.player.invincibil:
                return
            if self.game.player.alive:
                self.game.player.frame_index = 0
                sound = self.game.player.sounds.get(SoundType.EATEN, [])
                if len(sound) > 0:
                    sound[0].play()
            self.game.player.alive = False
            self.visible = False

    # def reset(self) -> None:
    #     super().reset()
        # self.mode = GhostMode.CHASE
        # print("name:",self.name, "mode:",self.mode, "alive:",self.alive)

    def after_death(self) -> None:
        self.mode = GhostMode.SPAWN
        self.goal = pg.Vector2(self.start_x, self.start_y)

    def reborn(self) -> None:
        if self.game.chase_phase:
            self.mode = GhostMode.CHASE
        else:
            self.mode = GhostMode.SCATTER
        self.alive = True
        self.visible = True
        self.dx = 0
        self.dy = 0
        self.teleport()

    def get_player_pos(self) -> pg.Vector2:
        return pg.Vector2(round(self.game.player.x), round(self.game.player.y))

    def get_player_direction(self) -> pg.Vector2:
        if not self.game.player.dx and not self.game.player.dy:
            return pg.Vector2(0, 0)
        if abs(self.game.player.dx) > abs(self.game.player.dy):
            return pg.Vector2(1 if self.game.player.dx > 0 else -1, 0)
        return pg.Vector2(0, 1 if self.game.player.dy > 0 else -1)

    def adjust_vector(self, vector: pg.Vector2) -> pg.Vector2:
        max_x = self.game.map.cols - 1
        max_y = self.game.map.rows - 1
        x = min(max(vector.x, 0), max_x)
        y = min(max(vector.y, 0), max_y)
        return pg.Vector2(x, y)

    def sound_init(self) -> None:
        self.sounds = Sound.read_sounds_from_files(
            "inc/sounds/ghosts/death/",
            SoundType.EATEN, self.sounds)
