import pygame as pg
from enum import Enum
import os

class FrameType(Enum):
    # stay / run / left / right / top / bottom / dead / 
    STAY = 1
    RUN = 2,
    LEFT = 3,
    RIGHT = 4,
    TOP = 5,
    BOTTOM = 6,
    DEAD = 7



class Entity:
    """Parent Class for NPC (Gosts) + Player (Pac-man) """

    def __init__(self, game, point=(0, 0), color=(50, 50, 50), name="Entity",size=11):
        self.game = game
        self.x, self.y = point
        self.name = name
        self.size = size  # radius
        self.dx = 0
        self.dy = 0
        self.color = color  # RGB() 
        self.frames: dict[FrameType, list[pg.Surface]] = {}
        self.frame_index = 0
        self.animation_timer = 0
        self.speed_factor = 0.04


    def movement(self):
        pass

    def update(self):
        self.movement()
        self.animation_timer += 0.1 + (abs(self.dx) + abs(self.dy))*self.speed_factor*5
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1

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
        
    def read_frames_from_file(self, file_path:str, frame_type: FrameType):
        path_ = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                file_path,
            )
        if os.path.exists(path_):
            files = sorted(
                f for f in os.listdir(path_)
                if f.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".bmp", ".webp")
                )
            )
            if len(self.frames.get(frame_type,[])) == 0:
                self.frames[frame_type] = []

            for filename in files:
                frame = pg.image.load(
                    os.path.join(path_, filename)
                ).convert_alpha()
                self.frames[frame_type].append(frame)
                print(filename)
            print(self.frames[frame_type])

            if not self.frames[frame_type]:
                print(f"No image files found in {path_}.")
        else:
            print(f"Can't find images files in {file_path} for {frame_type.name} of {self.name}.")
    