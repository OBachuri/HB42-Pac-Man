import pygame as pg
import pygame.gfxdraw as pggf
import math

from src.pc_entity import Entity, FrameType

class Player(Entity):
    """ Player = PacMan """
    def __init__(self, game, point=(0, 0), color=(250,250,10), name="PacMan", size=21):
        super().__init__(game, point=point, color=color, name=name, size=size)
        self.game = game
        self.angle = 0
        self.health = 100
        self.speed_factor = 0.01
        self.lives = 3

        try:
            self.teleport()
        except Exception:
            pass

        self.read_frames_from_file("inc/img/pacman/run/", FrameType.RUN)

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

    def check_walls(self, new_x, new_y, max_shift) -> bool:
        """ Returned True if there is wall on new palace """

        new_x_int = int(round(new_x, 0))
        new_y_int = int(round(new_y, 0))

        # (left or right) and (top ot bottom)
        if (((abs(new_x_int - new_x) <= max_shift)
             or (abs(new_y_int - new_y) <= max_shift))):
            return False

        # print("--- Diagonal = left:", (new_x_int > new_x), "top:", (new_y_int > new_y))
        if new_x_int > new_x:  # left
            # top
            if (((new_y_int > new_y)
                    and (self.game.map.world_map.get(
                        (new_x_int - 1, new_y_int - 1), 0) & 6 > 0))):
                # print("Top-Left (x,y): (",new_x_int - 1,",",new_y_int - 1,") w:", self.game.map.world_map.get((new_x_int - 1, new_y_int - 1), 0))
                return True
            # bottom
            elif (new_y_int < new_y) and (self.game.map.world_map.get(
                    (new_x_int - 1, new_y_int + 1), 0) & 3 > 0):
                # print("Bottom-Left (x,y): (",new_x_int - 1,",",new_y_int + 1,") w:", self.game.map.world_map.get((new_x_int - 1, new_y_int + 1), 0))
                return True
        else:  # Right
            # top
            if (((new_y_int > new_y)
                    and (self.game.map.world_map.get(
                        (new_x_int + 1, new_y_int - 1), 0) & 12 > 0))):
                # print("Top-Rigth (x,y): (",new_x_int + 1,",",new_y_int - 1,") w:", self.game.map.world_map.get((new_x_int + 1, new_y_int - 1), 0))
                return True
            # bottom
            elif (new_y_int < new_y) and (self.game.map.world_map.get(
                    (new_x_int + 1, new_y_int + 1), 0) & 9 > 0):
                # print("Bottom-Right (x,y): (",new_x_int + 1,",",new_y_int + 1,") w:", self.game.map.world_map.get((new_x_int + 1, new_y_int + 1), 0))
                return True
        return False

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
            # print("---- stop ----")
        if keys[pg.K_d] or keys[pg.K_p]:
            self.angle += 1
        if keys[pg.K_d] or keys[pg.K_o]:
            self.angle -= 1

        if (self.angle >= 360):
            self.angle = 0
        elif self.angle < 0:
            self.angle = 359

        if (dx == 0) and (dy == 0):
            self.dx = dx
            self.dy = dy
            return

        max_shift = round((((self.game.map.cell_size - self.size * 2 - 2) / 2)
                           / (self.game.map.cell_size
                              + self.game.map.wall_thickness)), 10)

        x = int(round(self.x, 0))
        y = int(round(self.y, 0))

        # if (self.x - x) > (max_shift + 1e-11):
        #     x += 1
        # if (self.y - y) > (max_shift + 1e-11):
        #     y += 1

        # w = self.game.map.world_map.get((x, y), 0)

        dx_sf = dx * self.speed_factor
        dy_sf = dy * self.speed_factor

        new_x = self.x + dx_sf
        new_y = self.y + dy_sf

        new_x_int = int(round(new_x, 0))
        new_y_int = int(round(new_y, 0))

        # if (new_x - new_x_int) > (max_shift + 1e-11):
        #     new_x_int += 1
        # if (new_y - new_y_int) > (max_shift + 1e-11):
        #     new_y_int += 1

        wn_d = self.game.map.world_map.get((new_x_int, new_y_int), 0)

        # print(f"new - int:({x},{y}), df:({dx},{dy}), new:({new_x},{new_y}), new_int:({new_x_int},{new_y_int})")

        # print(f"x-df: {new_x_int - new_x}, y-df: {new_y_int - new_y}")

        # if ((new_y_int - new_y) > max_shift):  # top
        #     if ((new_x_int - new_x) > max_shift):  # left
        #         print("top-left")
        #         if (self.game.map.world_map.get(
        #              (new_x_int - 1, new_y_int - 1), 0) & 9 > 0):
        #             dx = 0
        #             new_x = self.x
        #             dy = 0
        #             new_y = self.y
        #     elif ((new_x - new_x_int) > max_shift):  # right
        #         print("top-right")
        #         if self.game.map.world_map.get(
        #              (new_x_int + 1, new_y_int - 1), 0) & 3 > 0:
        #             dx = 0
        #             new_x = self.x
        #             dy = 0
        #             new_y = self.y
        # elif ((new_y - new_y_int) > max_shift):  # bottom
        #     if ((new_x_int - new_x) > max_shift):  # left
        #         print("bottom-left")
        #         if self.game.map.world_map.get(
        #              (new_x_int - 1, new_y_int + 1), 0) & 12 > 0:
        #             dx = 0
        #             new_x = self.x
        #             dy = 0
        #             new_y = self.y
        #     elif ((new_x - new_x_int) > max_shift):  # right
        #         print("bottom-right")
        #         if self.game.map.world_map.get(
        #              (new_x_int + 1, new_y_int + 1), 0) & 6 > 0:
        #             dx = 0
        #             new_x = self.x
        #             dy = 0
        #             new_y = self.y

        # left or rigth
        # if (abs(new_x_int - new_x) > max_shift):  # we are on the border by x
        #      if ((new_x_int - new_x) > max_shift):  # left border

        # left or rigth
        if (((((new_x_int - new_x) > max_shift) and (wn_d & 8 == 8))
             or (((new_x - new_x_int) > max_shift) and (wn_d & 2 == 2)))):
            # print("left or right (left = ", ((new_x_int - new_x) > max_shift), ")")
            dx = 0
            new_x = self.x
            new_x_int = x

        # top or bottom
        if (((((new_y_int - new_y) > max_shift) and (wn_d & 1 == 1))
             or (((new_y - new_y_int) > max_shift) and (wn_d & 4 == 4)))):
            dy = 0
            new_y = self.y
            new_y_int = y

        if self.check_walls(new_x, new_y, max_shift):
            if (dx != 0) and (dy != 0):
                if abs(dx) > abs(dy):
                    if self.check_walls(new_x, self.y, max_shift):
                        if self.check_walls(self.x, new_y, max_shift):
                            dy = 0
                            new_y = self.y
                            new_y_int = y
                        dx = 0
                        new_x = self.x
                        new_x_int = x
                    else:
                        dy = 0
                        new_y = self.y
                        new_y_int = y
                else:
                    if self.check_walls(self.x, new_y, max_shift):
                        if self.check_walls(new_x, self.y, max_shift):
                            dx = 0
                            new_x = self.x
                            new_x_int = x
                        dy = 0
                        new_y = self.y
                        new_y_int = y
                    else:
                        dx = 0
                        new_x = self.x
                        new_x_int = x
            else:
                dy = 0
                new_y = self.y
                dx = 0
                new_x = self.x


#            print("top or bottom (top = ", ((new_y_int - new_y) > max_shift))

        # (left or right) and (top ot bottom)
        # if (((abs(new_x_int - new_x) > max_shift)
        #      and (abs(new_y_int - new_y) > max_shift))):
        #     print("--- Diagonal = left:", (new_x_int > new_x), "top:", (new_y_int > new_y))
        #     if new_x_int > new_x:  # left
        #         # top
        #         if (((new_y_int > new_y)
        #              and (self.game.map.world_map.get(
        #                  (new_x_int - 1, new_y_int - 1), 0) & 6 > 0))):
        #             dy = 0
        #             new_y = self.y
        #             dx = 0
        #             new_x = self.x
        #             print("Top-Left (x,y): (",new_x_int - 1,",",new_y_int - 1,") w:", self.game.map.world_map.get((new_x_int - 1, new_y_int - 1), 0))
        #         # bottom
        #         elif (new_y_int < new_y) and (self.game.map.world_map.get(
        #              (new_x_int - 1, new_y_int + 1), 0) & 3 > 0):
        #             dy = 0
        #             new_y = self.y
        #             dx = 0
        #             new_x = self.x
        #             print("Bottom-Left (x,y): (",new_x_int - 1,",",new_y_int + 1,") w:", self.game.map.world_map.get((new_x_int - 1, new_y_int + 1), 0))
        #     else:  # Right
        #         # top
        #         if (((new_y_int > new_y)
        #              and (self.game.map.world_map.get(
        #                  (new_x_int + 1, new_y_int - 1), 0) & 12 > 0))):
        #             dy = 0
        #             new_y = self.y
        #             dx = 0
        #             new_x = self.x
        #             print("Top-Rigth (x,y): (",new_x_int + 1,",",new_y_int - 1,") w:", self.game.map.world_map.get((new_x_int + 1, new_y_int - 1), 0))
        #         # bottom
        #         elif (new_y_int < new_y) and (self.game.map.world_map.get(
        #              (new_x_int + 1, new_y_int + 1), 0) & 9 > 0):
        #             dy = 0
        #             new_y = self.y
        #             dx = 0
        #             new_x = self.x
        #             print("Bottom-Right (x,y): (",new_x_int + 1,",",new_y_int + 1,") w:", self.game.map.world_map.get((new_x_int + 1, new_y_int + 1), 0))



        # if (x != new_x_int) and (y != new_y_int):
        #     # Diagonal shift (Shift to the bottom-right corner)
        #     # Check top and left walls in cells that is in bottom-right corner
        #     wn_d = self.game.map.world_map.get((new_x_int, new_y_int), 0)
        #     if (wn_d & 9 > 0) or (w & 6 > 0):
        #         # there is wall on this corner
        #         if dx > dy:
        #             dy = 0
        #             new_y = self.y
        #         else:
        #             dx = 0
        #             new_x = self.x


        # print(f"before - cur:({self.x},{self.y}),int:({x},{y}, max_shift:{max_shift}, df({dx},{dy})")

        # if ((dy < 0) and (w & 1 == 1) and (new_y <= y - max_shift)):
        #     new_y = y - max_shift
        #     dy = 0
        # if ((dy > 0) and (w & 4 == 4) and (new_y >= y + max_shift)):
        #     new_y = y + max_shift
        #     dy = 0
        # if ((dx > 0) and (w & 2 == 2) and (new_x >= x + max_shift)):
        #     new_x = x + max_shift
        #     dx = 0
        # if ((dx < 0) and (w & 8 == 8) and (new_x <= x - max_shift)):
        #     new_x = x - max_shift
        #     dx = 0

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

        if (dx != 0) or (dy != 0):
            self.angle = math.degrees(math.atan2(-dy, dx)) % 360

 #       print(f"after - cur:({self.x},{self.y}),int:({x},{y}, max_shift:{max_shift}, df({dx},{dy})")


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
             + self.game.map.wall_thickness
             + self.game.map.top)


        frames = self.frames.get(FrameType.RUN, [])
        if len(frames) > 0:
            if self.frame_index >= len(frames):
                self.frame_index = 0
            image = frames[self.frame_index]
            if self.angle == 0:
                frame = image
            elif (self.angle == 180):
                frame = pg.transform.flip(image, True, False)
            elif (self.angle < 260) and (self.angle > 90):
                frame = pg.transform.flip(image, True, False)
                frame = pg.transform.rotate(frame, self.angle-180)
            else:
                frame = pg.transform.rotate(image, self.angle)
            
            rect = frame.get_rect(center=(int(x), int(y)))
            self.game.screen.blit(frame, rect)
        
        else:
        
            pg.draw.circle(self.game.screen,
                        self.color,
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

        self.game.screen.blit(self.game.font.render(
            f'x:{self.x}, y:{self.y}, a:{self.angle} ', False, (10, 10, 200)),
            (10, (self.game.map.rows + 1)
            * (self.game.map.step) + self.game.map.top))

        # x = (int(self.x) * (self.game.map.cell_size
        #                + self.game.map.wall_thickness)
        #      + self.game.map.cell_size / 2
        #      + self.game.map.wall_thickness)

        # y = (int(self.y) * (self.game.map.cell_size
        #                + self.game.map.wall_thickness)
        #      + self.game.map.cell_size / 2
        #      + self.game.map.wall_thickness)
        # pg.draw.circle(self.game.screen,
        #                'blue',
        #                (x,
        #                 y
        #                 ), 4)
