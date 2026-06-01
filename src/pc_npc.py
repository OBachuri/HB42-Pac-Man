import pygame as pg
import random
from enum import Enum
from src.pc_entity import Entity


class GhostMode(Enum):
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3
    STROLL = 4
    DEAD = 9  # SPAWN  


class NPC(Entity):
    """ Gosts """
    def __init__(self, game, point=(0, 0), color=(100, 100, 100), name="Gost", size=11):
        super().__init__(game,point=point,color=color,name=name,size=size)
        self.start_x, self.start_y = point
        self.angle = 0
        self.health = 100
        self.alive = True
        self.speed_factor = 0.04
        self.dx = 0
        self.dy = 0
        self.goal: tuple[int, int] | None = None
        self.start_chase_if_near = 5
        self.mode: GhostMode = GhostMode.CHASE

    def find_goal(self):
        x = int(round(self.x, 0))
        y = int(round(self.y, 0))

        # Check if player near and  ghosts not etable now
        if (self.mode == GhostMode.CHASE):
            self.goal = (int(round(self.game.player.x, 0)),
                         int(round(self.game.player.y, 0)))
        elif (((self.mode == GhostMode.STROLL)
                and ((self.game.player.x - x) ** 2
                     + (self.game.player.y - y) ** 2)
                < self.start_chase_if_near ** 2)):
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

    def teleport(self, x: int = -1, y: int = -1):
        if x < 0:
            x = self.start_x
        if y < 0:
            y = self.start_y
        self.x = int(x)
        self.y = int(y)

    def movement(self):

        keys = pg.key.get_pressed()
        if keys[pg.K_f]:
            self.mode = GhostMode.SCATTER

        x = self.x
        y = self.y

        if (((abs(int(round(x, 0)) - x) < self.speed_factor)
             and (abs(int(round(y, 0)) - y) < self.speed_factor))):
            x = int(round(x, 0))
            y = int(round(y, 0))

            # We in a center of the cell and must decide where to go
            self.find_goal()
            # Check if player near and not gosts etable now

            P_ = self.game.map.find_path((x, y), self.goal)
            # print("gost", self.name, "path:", P_)
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

        x = self.speed_factor * dx + self.x
        y = self.speed_factor * dy + self.y

        self.x = x
        self.y = y

    def update(self):
        self.movement()


class RedGhosts(NPC):
    """ Red gost (Blinky, Shadow)
        Blinky always chase his prey :)
    """
    def __init__(self, game,
                 point=(0, 0),
                 color=(250, 20, 20),
                 name="Red gost (Blinky, Shadow)"):
        super().__init__(game, point, color, name)

    def find_goal(self):
        x = int(round(self.x, 0))
        y = int(round(self.y, 0))

        # Check if player near and not gosts etable now
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
