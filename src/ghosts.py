from __future__ import annotations

import pygame as pg
import random
from collections.abc import Sequence
# from enum import Enum
from pc_entity import Entity, FrameType, GhostMode
from pc_sound import SoundType  # , Sound
from constants import FPS
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
        super().reset()
        self.mode = GhostMode.CHASE

    def find_goal(self) -> None:
        x = int(round(self.x, 0))
        y = int(round(self.y, 0))

        # Check if player near and not ghosts etable now
        if (((self.mode != GhostMode.FRIGHTENED)
             and (self.mode != GhostMode.SCATTER))):
            self.goal = (int(round(self.game.player.x, 0)),
                         int(round(self.game.player.y, 0)))
        elif ((self.mode == GhostMode.SCATTER)
              and (self.goal != (self.start_x, self.start_y))):
            self.goal = (self.start_x, self.start_y)
        else:
            if (self.goal is None) or self.goal == (x, y):
                # We have reached the goal and we need a new one
                if (self.mode == GhostMode.SCATTER):
                    self.mode = GhostMode.STROLL
                x_g = random.randrange(0, self.game.map.cols)
                y_g = random.randrange(0, self.game.map.rows)
                i = 20
                while (self.game.map.world_map.get((x_g, y_g), 0)
                        & 0xf == 0xf) and (i > 0):
                    x_g = random.randrange(0, self.game.map.cols)
                    y_g = random.randrange(0, self.game.map.rows)
                    i -= 1
                if i > 0:
                    self.goal = (x_g, y_g)
                # print(self.name, " goal=", self.goal)


class PinkGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (240, 24, 140), "Pink ghost (Speedy)")
        self.read_frames_from_file("inc/img/pink/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/pink/stay/", FrameType.STAY)

    def reset(self) -> None:
        super().reset()
        self.mode = GhostMode.CHASE

    # def find_goal(self) -> None:
    #     x = int(round(self.x, 0))
    #     y = int(round(self.y, 0))

    #     # Check if player near and not ghosts etable now
    #     if (((self.mode != GhostMode.FRIGHTENED)
    #          and (self.mode != GhostMode.SCATTER))):
    #         self.goal = (int(round(self.game.player.x, 0)),
    #                      int(round(self.game.player.y, 0)))
    #     elif ((self.mode == GhostMode.SCATTER)
    #           and (self.goal != (self.start_x, self.start_y))):
    #         self.goal = (self.start_x, self.start_y)
    #     else:
    #         if (self.goal is None) or self.goal == (x, y):
    #             # We have reached the goal and we need a new one
    #             if (self.mode == GhostMode.SCATTER):
    #                 self.mode = GhostMode.STROLL
    #             x_g = random.randrange(0, self.game.map.cols)
    #             y_g = random.randrange(0, self.game.map.rows)
    #             i = 20
    #             while (self.game.map.world_map.get((x_g, y_g), 0)
    #                     & 0xf == 0xf) and (i > 0):
    #                 x_g = random.randrange(0, self.game.map.cols)
    #                 y_g = random.randrange(0, self.game.map.rows)
    #                 i -= 1
    #             if i > 0:
    #                 self.goal = (x_g, y_g)


class CyanGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (100, 250, 250),
                         "Cyan ghost (Inky, Bashful)")
        self.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/cyan/stay/", FrameType.STAY)

    def reset(self) -> None:
        super().reset()
        self.mode = GhostMode.CHASE

    # def find_goal(self) -> None:
    #     x = int(round(self.x, 0))
    #     y = int(round(self.y, 0))

    #     # Check if player near and not ghosts etable now
    #     if (((self.mode != GhostMode.FRIGHTENED)
    #          and (self.mode != GhostMode.SCATTER))):
    #         self.goal = (int(round(self.game.player.x, 0)),
    #                      int(round(self.game.player.y, 0)))
    #     elif ((self.mode == GhostMode.SCATTER)
    #           and (self.goal != (self.start_x, self.start_y))):
    #         self.goal = (self.start_x, self.start_y)
    #     else:
    #         if (self.goal is None) or self.goal == (x, y):
    #             # We have reached the goal and we need a new one
    #             if (self.mode == GhostMode.SCATTER):
    #                 self.mode = GhostMode.STROLL
    #             x_g = random.randrange(0, self.game.map.cols)
    #             y_g = random.randrange(0, self.game.map.rows)
    #             i = 20
    #             while (self.game.map.world_map.get((x_g, y_g), 0)
    #                     & 0xf == 0xf) and (i > 0):
    #                 x_g = random.randrange(0, self.game.map.cols)
    #                 y_g = random.randrange(0, self.game.map.rows)
    #                 i -= 1
    #             if i > 0:
    #                 self.goal = (x_g, y_g)


class OrangeGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (250, 120, 10),
                         "Orange ghost (Clyde, Pockey)")
        self.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/orange/stay/", FrameType.STAY)

    def reset(self) -> None:
        super().reset()
        self.mode = GhostMode.CHASE

    # def find_goal(self) -> None:
    #     x = int(round(self.x, 0))
    #     y = int(round(self.y, 0))

    #     # Check if player near and not ghosts etable now
    #     if (((self.mode != GhostMode.FRIGHTENED)
    #          and (self.mode != GhostMode.SCATTER))):
    #         self.goal = (int(round(self.game.player.x, 0)),
    #                      int(round(self.game.player.y, 0)))
    #     elif ((self.mode == GhostMode.SCATTER)
    #           and (self.goal != (self.start_x, self.start_y))):
    #         self.goal = (self.start_x, self.start_y)
    #     else:
    #         if (self.goal is None) or self.goal == (x, y):
    #             # We have reached the goal and we need a new one
    #             if (self.mode == GhostMode.SCATTER):
    #                 self.mode = GhostMode.STROLL
    #             x_g = random.randrange(0, self.game.map.cols)
    #             y_g = random.randrange(0, self.game.map.rows)
    #             i = 20
    #             while (self.game.map.world_map.get((x_g, y_g), 0)
    #                     & 0xf == 0xf) and (i > 0):
    #                 x_g = random.randrange(0, self.game.map.cols)
    #                 y_g = random.randrange(0, self.game.map.rows)
    #                 i -= 1
    #             if i > 0:
    #                 self.goal = (x_g, y_g)
