import sys
import random
# from typing import cast
# import os

try:
    import pygame as pg
    # from pydantic import ValidationError
except ModuleNotFoundError as e:
    print("\nError: One of the dependencies is missing\n", e)
    print("Please run 'make install'")
    sys.exit(1)

# from src.pc_map import Map
# from src.pc_player import Player
from src.pc_game import Game
from src.pc_npc import NPC, RedGhosts
from src.pc_entity import FrameType
from src.pc_artifact import PowerPellet, Pellet
from src.parser import Config, Parser

# RES = WIDTH, HEIGHT = 1000, 800
# FPS = 0


def main() -> int:
    if len(sys.argv) != 2:
        print("\nError: Invalid program launch format" +
              "\nUsage 'python3 ./pac-man.py <config-file-path>'")
        sys.exit(1)

    config: Config = Parser.get_config(sys.argv[1])

    maze_ = []

    # try our maze generator
    # try:
    #     from mazegen import CMazeParams, MazeGenerator, CAlg
    #     our_mazgen = True
    # except Exception as err_msg:
    #     our_mazgen = False
    #     # print("Error with mazegen library connection:", err_msg)
    #     # sys.exit(1)

    # random.seed(1)

    # try shcool maze generator
    try:
        print("*"*40)
        from mazegenerator.mazegenerator import MazeGenerator
        # from mazegenerator import MazeGenerator
    except Exception as err_msg:
        print("Error with mazegen library connection:", err_msg)
        print("Check for the presence of the package " +
              "and run 'make install' again.")
        sys.exit(1)

    print("Maze generation - start  ...")
    # temporary first level (config.levels[0])
    maze_ = MazeGenerator(size=config.levels[0].size,
                          exit_cell=(0, 1),
                          seed=config.levels[0].seed).maze
    print("Maze generation - end")

    pg.init()
    pg.font.init()
    pg.mixer.init()

    game = Game(config)
    Pellet.sound_init()
    # print(game.map.world_map)
    print("*"*30)

    # print(pg.font.get_fonts())
    game.map.print(maze_)

    maze_ = game.map.do_not_prefect(maze_)

    # game.map.get_map_form_file(c_mz_param.output_file)
    game.map.get_map(maze_)
    game.map.print()

    game.player.teleport()
    game.npcs.append(RedGhosts(game))

    pink = NPC(game, (game.map.cols - 1, 0),
               (240, 24, 140), "Pink gost (Speedy)")
    game.npcs.append(pink)
    pink.read_frames_from_file("inc/img/pink/run/", FrameType.RUN)

    cyan = NPC(game,
               (game.map.cols - 1, game.map.rows - 1),
               (100, 250, 250), "Cyan gost (Inky, Bashful)")
    game.npcs.append(cyan)
    cyan.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)

    orange = NPC(game,
                 (0, game.map.rows - 1),
                 (250, 120, 10), "Orange gost (Clyde, Pockey)")
    game.npcs.append(orange)
    orange.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)

    game.npcs[0].goal = (game.player.x, game.player.y)
    game.npcs[1].goal = (game.player.x, game.player.y)
    game.npcs[2].goal = (game.player.x, game.player.y)
    game.npcs[3].goal = (game.player.x, game.player.y)

    #  Add PowerPellet and Pellet
    game.artifacts.append(PowerPellet(game, (0, 0)))
    game.artifacts.append(PowerPellet(game, (game.map.cols - 1, 0)))
    game.artifacts.append(PowerPellet(game,
                                      (game.map.cols - 1, game.map.rows - 1)))
    game.artifacts.append(PowerPellet(game, (0, game.map.rows - 1)))

    place_set = {(x, y) for x in range(0, game.map.cols)
                 for y in range(0, game.map.rows)
                 if (game.map.world_map.get((x, y), 0) & 15 != 15)}

    for a_ in game.artifacts:
        place_set.remove((a_.x, a_.y))

    if config.pacgum <= 0:
        for s_ in place_set:
            game.artifacts.append(Pellet(game, s_))
    else:
        for p in range(0, config.pacgum):
            if (len(place_set) < 1):
                print("All Pellets can't be placed "
                      f"({p+1} from {config.pacgum}).")
                break
            x, y = random.choice(tuple(place_set))
            game.artifacts.append(Pellet(game, (x, y)))
            place_set.remove((x, y))

    # print(game.map.world_map)
    game.screen = pg.display.set_mode(
        (max(game.map.cols*game.map.step
         + game.map.wall_thickness, 550),
         (game.map.rows + 3)*(game.map.step)))
    # print(dir(pg.draw))
    game.run()

    return (0)


if __name__ == "__main__":
    main()
