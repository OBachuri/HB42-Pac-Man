import pygame as pg
# from typing import cast
from pydantic import ValidationError
import sys
# import os

from mazegen import CMazeParams, MazeGenerator, CAlg
# from src.pc_map import Map
# from src.pc_player import Player
from src.pc_game import Game

# RES = WIDTH, HEIGHT = 1000, 800
# FPS = 0


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
    game.player.teleport()
    # print(game.map.world_map)
    game.screen = pg.display.set_mode(
        (game.map.cols*(game.map.cell_size+game.map.wall_thickness)
         + game.map.wall_thickness,
         (game.map.rows + 3)*(game.map.cell_size+game.map.wall_thickness)))
    # print(dir(pg.draw))
    game.run()

    return (0)


if __name__ == "__main__":
    main()
