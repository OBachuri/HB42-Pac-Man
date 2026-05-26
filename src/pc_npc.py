import pygame as pg
import random


class NPC:
    """ Gosts """
    def __init__(self, game, point=(0, 0), color=(100, 100, 100), name="Gost"):
        self.game = game
        self.x, self.y = point
        self.start_x, self.start_y = point
        self.angle = 0
        self.health = 100
        self.alive = True
        self.size = 11  # radius
        self.speed_factor = 0.06
        self.dx = 0
        self.dy = 0
        self.color = color
        self.name = name
        self.goal = None
        self.start_chase_if_near = 5

    def movement(self):
        x = self.x
        y = self.y

        if (((abs(int(round(x, 0)) - x) < self.speed_factor)
             and (abs(int(round(y, 0)) - y) < self.speed_factor))):
            x = int(round(x, 0))
            y = int(round(y, 0))

            # We in a center of the cell and must decide where to go
            # Check if player near and not gosts etable now
            if (((self.game.gost_edible == 0)
                 and ((self.game.player.x - x) ** 2
                      + (self.game.player.y - y) ** 2)
                 < self.start_chase_if_near ** 2)):
                self.goal = (int(round(self.game.player.x, 0)),
                             int(round(self.game.player.y, 0)))
            else:
                if (self.goal is None) or self.goal == (x, y):
                    # We have reached the goal and we need a new one
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

    def draw(self):
        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness)

        y = (self.y * (self.game.map.step)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        pg.draw.circle(self.game.screen,
                       self.color,
                       (x, y), self.size)

    def update(self):
        self.movement()


class RedGhosts(NPC):

    def __init__(self, game,
                 point=(0, 0),
                 color=(250, 20, 20),
                 name="Red gost (Blinky, Shadow)"):
        super().__init__(game, point, color, name)
