from __future__ import annotations

import pygame as pg
import random

# from collections.abc import Sequence
# from enum import Enum

from pc_entity import FrameType, GhostMode  # Entity
# from pc_sound import SoundType  # , Sound
# from pc_constants import FPS
from pc_npc import NPC

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class RedGhost(NPC):
    """ Red ghost (Blinky, Shadow)
        Blinky always chase his prey :)
    """

    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (250, 20, 20),
                         "Red ghost (Blinky, Shadow)")
        self.read_frames_from_file("inc/img/red/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/red/stay/", FrameType.STAY)

    def reset(self) -> None:
        self.start_x = 0
        self.start_y = 0
        self.mode = GhostMode.CHASE
        super().reset()

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            self.goal = self.get_player_pos()
        else:
            super().find_goal()


class PinkGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0),
                 red_ghost: NPC | None = None) -> None:
        super().__init__(game, point, (240, 24, 140), "Pink ghost (Speedy)")
        self.red_ghost = red_ghost
        self.tiles: int = 4
        self.read_frames_from_file("inc/img/pink/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/pink/stay/", FrameType.STAY)

    def reset(self) -> None:
        self.start_x = self.game.map.cols - 1
        self.start_y = 0
        self.mode = GhostMode.CHASE
        super().reset()
        # print("reset:", self.name, "x:", self.x, "y:",
        #       self.y, "vis:", self.visible,
        #       ",goal:", self.goal, ",start:", (self.start_x, self.start_y),
        #       "speed:", self.speed_factor)

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            pos = pg.Vector2(self.x, self.y)
            red_ghost_pos = pg.Vector2(
                self.red_ghost.x, self.red_ghost.y) if self.red_ghost else None
            player_pos = self.get_player_pos()
            player_direction = 0

            if (pos.distance_to(player_pos) <= self.start_chase_if_near and
               red_ghost_pos is not None
               and red_ghost_pos.distance_to(
                   player_pos) > self.start_chase_if_near):
                self.goal = player_pos
                return
            player_direction = self.get_player_direction()
            if player_direction:
                tiles = self.tiles
                self.goal = self.adjust_vector(
                    player_pos + player_direction * tiles)
                while not self.game.map.has_cell_exit(int(self.goal.x),
                                                      int(self.goal.y)):
                    tiles -= 1
                    if tiles > 0:
                        self.goal = self.adjust_vector(
                            player_pos + player_direction * tiles)
                    else:
                        self.goal = player_pos
            else:
                self.goal = player_pos
        else:
            super().find_goal()


class CyanGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0),
                 red_ghost: NPC | None = None) -> None:
        super().__init__(game, point, (100, 250, 250),
                         "Cyan ghost (Inky, Bashful)")
        self.red_ghost = red_ghost
        self.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/cyan/stay/", FrameType.STAY)

    def reset(self) -> None:
        self.start_x = self.game.map.cols - 1
        self.start_y = self.game.map.rows - 1
        self.mode = GhostMode.CHASE
        super().reset()

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            player_pos = self.get_player_pos()
            red_ghost_pos = pg.Vector2(0, 0)
            if self.red_ghost:
                red_ghost_pos = pg.Vector2(round(self.red_ghost.x),
                                           round(self.red_ghost.y))

            # position 2 tiles in front of the player
            vec1 = self.adjust_vector(
                player_pos + self.get_player_direction() * 2)
            # vector for red ghost to reach vec1
            vec2 = (vec1 - red_ghost_pos)
            self.goal = self.adjust_vector(red_ghost_pos + vec2 * 2)

            i = 10
            while not self.game.map.has_cell_exit(int(self.goal.x),
                                                  int(self.goal.y)):
                # reduce vec2
                if vec2.x < 0:
                    vec2.x += 1
                else:
                    vec2.x -= 1
                if vec2.y < 0:
                    vec2.y += 1
                else:
                    vec2.y -= 1

                self.goal = self.adjust_vector(red_ghost_pos + vec2 * 2)

                if self.goal == vec1 or (i < 0):
                    self.goal = player_pos
                    return
                i -= 1
        else:
            super().find_goal()


class OrangeGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (250, 120, 10),
                         "Orange ghost (Clyde, Pockey)")
        # self.tiles = int(min(self.game.map.cols, self.game.map.rows) * 0.42)
        self.tiles: int = 4
        self.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/orange/stay/", FrameType.STAY)

        # for mypy test - it can't check type from NPC
        self.goal: pg.Vector2 | None = None

    def reset(self) -> None:
        self.start_x = 0
        self.start_y = self.game.map.rows - 1
        self.goal = None
        self.mode = GhostMode.CHASE
        super().reset()

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            if (self.goal is not None
               and self.goal != (round(self.x), round(self.y))):
                return
            player_pos = self.get_player_pos()
            x = int(player_pos.x)
            y = int(player_pos.y)

            max_x = self.game.map.cols - 1
            max_y = self.game.map.rows - 1
            pos_x_min = max(0, x - self.tiles)
            pos_x_max = min(x + self.tiles, max_x)
            pos_y_min = max(0, y - self.tiles)
            pos_y_max = min(y + self.tiles, max_y)

            vecs: list[pg.Vector2] = []
            if (y > self.tiles):
                vecs.extend([pg.Vector2(x, pos_y_min) for x
                             in range(pos_x_min, pos_x_max + 1)
                             if self.game.map.has_cell_exit(x, pos_y_min)])
            if (max_y - y > self.tiles):
                vecs.extend([pg.Vector2(x, pos_y_max) for x
                             in range(pos_x_min, pos_x_max + 1)
                             if self.game.map.has_cell_exit(x, pos_y_max)])
            if x > self.tiles:
                vecs.extend([pg.Vector2(pos_x_min, y) for y
                             in range(pos_y_min + 1, pos_y_max)
                             if self.game.map.has_cell_exit(pos_x_min, y)])
            if max_x - x > self.tiles:
                vecs.extend([pg.Vector2(pos_x_max, y) for y
                            in range(pos_y_min + 1, pos_y_max)
                            if self.game.map.has_cell_exit(pos_x_max, y)])
            if len(vecs):
                self.goal = random.choice(vecs)
            else:
                self.goal = pg.Vector2(self.start_x, self.start_y)
        else:
            super().find_goal()
