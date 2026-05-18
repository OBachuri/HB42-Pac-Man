import pygame as pg
import pygame.gfxdraw as pggf
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = 1, 1
        self.angle = 0
        self.health = 100
        self.size = 11  # radius
        self.speed_factor = 0.01
        self.dx = 0
        self.dy = 0

        try:
            self.teleport()
        except Exception:
            pass

    def teleport(self, x: int = -1, y: int = -1):
        if x < 0:
            x = int(self.game.map.cols / 2)
        if y < 0:
            y = int(self.game.map.rows / 2)
        while (self.game.map.world_map.get((x, y), 0) & 15 == 15) and (x > 0):
            x -= 1
        if (((x < 0) or (y < 0)
             or (x >= self.game.map.cols) or (y >= self.game.map.rows))):
            return
        self.x = int(x)
        self.y = int(y)

    def check_wall(self, x, y):
        pass

    def movement(self):
        num_key_pressed = -1
        dx = self.dx
        dy = self.dy
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            num_key_pressed += 1
            dy += -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            num_key_pressed += 1
            dy += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            num_key_pressed += 1
            dx += -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            num_key_pressed += 1
            dx += 1
        if keys[pg.K_SPACE]:
            dx = 0
            dy = 0
        if keys[pg.K_d] or keys[pg.K_p]:
            self.angle += 0.1
        if keys[pg.K_d] or keys[pg.K_o]:
            self.angle -= 0.1

        if (self.angle >= 2 * math.pi):
            self.angle = 0
        elif self.angle < 0:
            self.angle = 2 * math.pi - 0.1

        if (dx == 0) and (dy == 0):
            self.dx = dx
            self.dy = dy
            return

        max_shift = round((((self.game.map.cell_size - self.size * 2 - 2) / 2)
                           / (self.game.map.cell_size
                              + self.game.map.wall_thickness)), 10)

        x = int(self.x)
        if (self.x - x) > (max_shift + 1e-11):
            x += 1
        y = int(self.y)
        if (self.y - y) > (max_shift + 1e-11):
            y += 1
        w = self.game.map.world_map.get((x, y), 0)

        print(f"before - cur:({self.x},{self.y}),int:({x},{y}, max_shift:{max_shift}, df({dx},{dy})")

        dx_sf = dx * self.speed_factor
        dy_sf = dy * self.speed_factor

        new_x = self.x + dx_sf
        new_y = self.y + dy_sf

        new_x_int = int(new_x)
        if (new_x - new_x_int) > (max_shift + 1e-11):
            new_x_int += 1
        new_y_int = int(new_y)
        if (new_y - new_x_int) > (max_shift + 1e-11):
            new_y_int += 1

        if (new_x != x) and (new_y != y):
            # diagonal move to new cell
            pass

        if ((dy < 0) and (w & 1 == 1) and (new_y <= y - max_shift)):
            new_y = y - max_shift
            dy = 0
        if ((dy > 0) and (w & 4 == 4) and (new_y >= y + max_shift)):
            new_y = y + max_shift
            dy = 0
        if ((dx > 0) and (w & 2 == 2) and (new_x >= x + max_shift)):
            new_x = x + max_shift
            dx = 0
        if ((dx < 0) and (w & 8 == 8) and (new_x <= x - max_shift)):
            new_x = x - max_shift
            dx = 0

        self.x = new_x
        self.y = new_y

        if (self.x <= - max_shift):
            self.x = - max_shift
            dx = 0
        elif (self.x >= (self.game.map.cols - 1) + max_shift):
            self.x = self.game.map.cols - 1 + max_shift
            dx = 0

        if (self.y < - max_shift):
            self.y = - max_shift
            dy = 0
        elif (self.y > (self.game.map.rows - 1) + max_shift):
            self.y = self.game.map.rows - 1 + max_shift
            dy = 0

        self.dx = dx
        self.dy = dy

 #       print(f"after - cur:({self.x},{self.y}),int:({x},{y}, max_shift:{max_shift}, df({dx},{dy})")

    def update(self):
        self.movement()

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * (self.game.map.self.cell_size + self.game.map.wall_thickness), self.y * (self.game.map.self.cell_size + self.game.map.wall_thickness)),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #              self.y * 100 + WIDTH * math. sin(self.angle)), 2)

        x = (self.x * (self.game.map.cell_size
                       + self.game.map.wall_thickness)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness)

        y = (self.y * (self.game.map.cell_size
                       + self.game.map.wall_thickness)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness)

        pg.draw.circle(self.game.screen,
                       'yellow',
                       (x, y), self.size)
        # eye
        # print("angle:", math.degrees(self.angle))
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        pg.draw.circle(self.game.screen,
                       'black',
                       (x + 5 * sin_a,
                        y - 5 * cos_a
                        ), 3)
        # mouth = jaws
        pggf.pie(self.game.screen, int(x), int(y), self.size,
                 -20, 20, (255, 0, 0))
        self.game.screen.blit(self.game.font.render(f'x:{self.x}, y:{self.y}', False, (10, 10, 200)), (10,10))
