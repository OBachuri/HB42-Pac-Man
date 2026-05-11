import pygame as pg
# from typing import cast
from pydantic import ValidationError
import sys
# import os

from mazegen import CMazeParams, MazeGenerator, CAlg
from src.pc_map import Map

# RES = WIDTH, HEIGHT = 1000, 800
FPS = 0


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((800, 800))
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)

    def update(self):
        # self.player.update()
        # self.raycasting.update()
        # self.object_handler.update()
        # self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        # self.object_renderer.draw()
        # self.weapon.draw()
        self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            # self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


def main() -> int:
    try:
        c_mz_param = CMazeParams(width=20,
                                 height=15,
                                 entry=(0, 0),
                                 exit=(0, 1),
                                 output_file="maze_txt.txt",
                                 perfect=False,
                                 insert_42=True,
                                 algorithm=CAlg.DFS
                                 )
    except ValidationError as e:
        # for err in e.errors():
        #     print(err["msg"])
        print(e, file=sys.stderr)
        sys.exit(1)

    print("Maze config:", c_mz_param.print())
    maze_ = MazeGenerator.generate(c_mz_param)
    MazeGenerator.write_to_file(maze_, c_mz_param, [])
    print(f"The maze saved to file '{c_mz_param.output_file}'")

    game = Game()
    # print(game.map.world_map)
    # print("*"*30)
    game.map.get_map_form_file(c_mz_param.output_file)
    # print(game.map.world_map)
    game.screen = pg.display.set_mode(
        (game.map.cols*(game.map.cell_size+game.map.wall_thickness)
         + game.map.wall_thickness,
         (game.map.rows + 3)*(game.map.cell_size+game.map.wall_thickness)))
    game.run()

    return (0)


if __name__ == "__main__":
    main()
