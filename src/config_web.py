from typing import Any

import pygame as pg

from pc_artifact import BonusFruitType


class LevelWeb:
    def __init__(self, data: dict[str, Any] = {}) -> None:
        self.number: int = 1
        self.map_filename: str = ""
        self.remove_deadends: bool = True
        self.width: int = 14
        self.height: int = 10
        self.seed: int = 0
        self.level_max_time: int = 120
        self.speed_factor_player: float = 0.01
        self.speed_factor_ghost: float = 0.02
        self.max_player_acceleration: int = 5
        self.points_per_bonus_fruit: int = 100
        self.bonus_fruit_type: BonusFruitType = BonusFruitType.CHERRY
        self.walls_color: tuple[int, ...] = (40, 200, 40)
        self.pacgum: int = 0

        try:
            n = int(data.get("number", 1))
            if n < 0:
                raise ValueError("Number of level must be positive integer")
            self.number = n
        except Exception as ex:
            print("Error in config in level number =",
                  data.get("number", 1), ":", ex)

        try:
            str_ = str(data.get("map_filename", ""))
            self.map_filename = str_
        except Exception as ex:
            print(f"Error in config for level {self.number} "
                  "- wrong map file name",
                  data.get("map_filename", ""), ":", ex)

        try:
            self.remove_deadends = bool(data.get("remove_deadends", True))
        except Exception as ex:
            print(f"Error: Wrong value remove_deadends for level"
                  f"(level:{self.number})! \n", ex)

        try:
            v = int(data.get("width", 14))
            if v < 3 or v > 40:
                print(f'Error: Wrong value "width"={v} (3-25) for level'
                      f"(level:{self.number})! \n")
                v = 14
            self.width = v
        except Exception as ex:
            print(f'Error: Wrong value "width" (3-25) for level'
                  f"(level:{self.number})! \n", ex)

        try:
            v = int(data.get("height", 14))
            if v < 3 or v > 30:
                print(f'Error: Wrong value "height"={v} (3-25) for level'
                      f"(level:{self.number})! \n")
                v = 10
            self.height = v
        except Exception as ex:
            print(f'Error: Wrong value "height" (3-25) for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.seed = int(data.get("seed", 0))
        except Exception as ex:
            print(f'Error: Wrong value "seed" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.pacgum = int(data.get("pacgum", 0))
        except Exception as ex:
            print(f'Error: Wrong value "pacgum" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.level_max_time = max(10, int(data.get("level_max_time", 90)))
        except Exception as ex:
            print(f'Error: Wrong value "level_max_time" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.speed_factor_player = min(max(
                float(data.get("speed_factor_player", 0.01)), 0.005), 10)
        except Exception as ex:
            print(f'Error: Wrong value "speed_factor_player" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.speed_factor_ghost = min(max(float(data.get(
                "speed_factor_ghost", 0.02)), 0.01), 0.5)
        except Exception as ex:
            print(f'Error: Wrong value "speed_factor_ghost" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.max_player_acceleration = min(max(int(data.get(
                "max_player_acceleration", 5)), 1), 100)
        except Exception as ex:
            print(f'Error: Wrong value "max_player_acceleration" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            self.points_per_bonus_fruit = max(int(data.get(
                "points_per_bonus_fruit", 100)), 0)
        except Exception as ex:
            print(f'Error: Wrong value "points_per_bonus_fruit" for level'
                  f"(level:{self.number})! \n", ex)

        try:
            f_nane = str(data.get("bonus_fruit_type", "cherry"))
            fruit = BonusFruitType[f_nane.upper()]
            self.bonus_fruit_type = fruit
        except Exception as ex:
            print("Error: Can't find fruit: ", f_nane,
                  f"(level:{self.number})!", ex)

        try:
            color_txt = str(data.get("walls_color", "green"))
            self.walls_color = tuple(pg.Color(color_txt)[:3])
        except Exception as ex:
            print(f"Error: Wrong color of wall for level"
                  f"(level:{self.number})!", ex)

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)

    def print(self) -> None:
        print("--Level:")
        print("Number:", self.number)
        print("Width:", self.width)
        print("Height:", self.height)
        print("Map File:", self.map_filename)
        print("Seed:", self.seed)
        print("Remove deadends:", self.remove_deadends)
        print("Time max:", self.level_max_time, "s")
        print("walls color:", self.walls_color)


class ConfigWeb:
    def __init__(self, cfg_data: dict[str, Any] = {}) -> None:

        self.highscores_filename: str = "highscores.json"
        self.lives: int = 3
        self.points_per_pacgum: int = 10
        self.points_per_super_pacgum: int = 50
        self.points_per_ghost: int = 200
        self.seed: int = 0

        try:
            str_ = str(cfg_data.get("highscores_filename", "highscores.json"))
            if len(str_) > 5:
                self.highscores_filename = str_
            else:
                print("Error: Wrong value of highscores_filename -", str_)
        except Exception as ex:
            print("Error: Wrong value of highscores_filename -", ex)

        try:
            l_ = int(cfg_data.get("lives", 3))
            if (l_ > 0):
                self.lives = l_
            else:
                print("Error: Wrong value of lives -", l_)
        except Exception as ex:
            print("Error: Wrong value of lives -", ex)

        try:
            p_ = int(cfg_data.get("points_per_pacgum", 10))
            if (p_ >= 0):
                self.points_per_pacgum = p_
            else:
                print("Error: Wrong value of points_per_pacgum -", p_)
        except Exception as ex:
            print("Error: Wrong value of points_per_pacgum -", ex)

        try:
            p_ = int(cfg_data.get("points_per_super_pacgum", 50))
            if (p_ >= 0):
                self.points_per_super_pacgum = p_
            else:
                print("Error: Wrong value of points_per_super_pacgum -", p_)
        except Exception as ex:
            print("Error: Wrong value of points_per_super_pacgum -", ex)

        try:
            p_ = int(cfg_data.get("points_per_ghost", 200))
            if (p_ >= 0):
                self.points_per_ghost = p_
            else:
                print("Error: Wrong value of points_per_ghost -", p_)
        except Exception as ex:
            print("Error: Wrong value of points_per_ghost -", ex)

        try:
            self.seed = int(cfg_data.get("seed", 0))
        except Exception as ex:
            print("Error: Wrong value of seed -", ex)

        self.cheat: bool = False
        try:
            self.cheat = bool(cfg_data.get("cheat", False))
        except Exception as ex:
            print("Error: Wrong value for cheat - ", ex)

        self.fullscreen_mode: bool = False
        try:
            self.fullscreen_mode = bool(cfg_data.get("fullscreen_mode", False))
        except Exception as ex:
            print("Error: Wrong value of fullscreen_mode - ", ex)

        try:
            levels: list[LevelWeb] = [LevelWeb(level_data)
                                      for level_data
                                      in cfg_data.get("levels", [])]
            min_level = 0
            min_level = min({l_.number for l_ in levels})
            if min_level != 1:
                print("Error: in config must be Level number 1!")
                levels.append(LevelWeb())
        except Exception as ex:
            print("Error in config for levels:", ex)
            levels = []

        self.levels: list[LevelWeb] = levels if levels else [LevelWeb()]

    def print(self) -> None:
        print("--Config:")
        print("Seed:", self.seed)
        print("Cheat:", self.cheat)
        print("Levels: ", len(self.levels))
        for l_ in self.levels:
            l_.print()
