import pygame as pg
from enum import Enum
import os


class FrameType(Enum):
    # stay / run / left / right / top / bottom / dead / frightened
    STAY = 1
    RUN = 2,
    LEFT = 3,
    RIGHT = 4,
    UP = 5,
    DOWN = 6,
    DEATH = 7,
    DEAD = 8,
    FRIGHTENED = 9,
    END_OF_FRIGHTENED = 10,


class GhostMode(Enum):
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3
    STROLL = 4
    DEAD = 9
    SPAWN = 10


class Entity:
    """Parent Class for NPC (Gosts) + Player (Pac-man) """

    def __init__(self, game, point=(0, 0),
                 color=(50, 50, 50), name="Entity", size=11):
        self.game = game
        self.x, self.y = point
        self.start_x, self.start_y = point
        self.name = name
        self.size = size  # radius
        self.alive = True
        self.dx = 0
        self.dy = 0
        self.color = color  # (R,G,B)
        self.frames: dict[FrameType, list[pg.Surface]] = {}
        self.mode: GhostMode = GhostMode.STROLL
        self.frame_index = 0
        self.animation_timer = 0
        self.event_timer = 0
        self.speed_factor = 0.04
        self.visible = True
        self.max_d = 5  # max dx + dy

    def reset(self):
        self.dx = 0
        self.dy = 0
        self.teleport()
        self.frame_index = 0
        self.animation_timer = 0
        self.alive = True
        self.visible = True

    def teleport(self, x: int = -1, y: int = -1):
        if x < 0:
            x = self.start_x
        if y < 0:
            y = self.start_y
        self.x = int(x)
        self.y = int(y)

    def movement(self):
        pass

    def update(self):
        self.movement()
        if self.alive:
            self.animation_timer += 0.1
            + (abs(self.dx) + abs(self.dy)) * self.speed_factor*5
        else:
            self.animation_timer += 0.1
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1

    def collide_check(self, o_: "Entity"):
        x = o_.x
        y = o_.y
        s = o_.size
        # print("o(x,y,s)",x,y,s,f"{o_.name}^{self.name}",
        # " c(x,y,s)", self.x,self.y,self.size)
        # print(((self.x - x)**2 + (self.y - y)**2))
        # print(((self.size + s)/self.game.map.step)**2)
        return (((self.x - x)**2
                + (self.y - y)**2)
                < ((self.size + s)/self.game.map.step)**2)

    def draw(self):

        if not (self.visible):
            return

        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness)

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
                if not (self.alive):
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

    def after_death(self):
        pass

    def read_frames_from_file(self, file_path: str, frame_type: FrameType):
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
