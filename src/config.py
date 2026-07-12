from typing import ClassVar, Any
from pydantic import BaseModel
from pydantic import PositiveInt, NonNegativeInt, PositiveFloat
from pydantic import field_validator

import pygame as pg

from pc_artifact import BonusFruitType


class Level(BaseModel):
    """Per-level gameplay and maze configuration.

    Defines level geometry, timing, movement tuning, collectible values,
    bonus fruit settings, and visual options. Validators coerce invalid
    inputs to safe defaults to prevent runtime failures.

    Attributes:
        map_filename (str): Optional path to a predefined maze file.
        number (PositiveInt): Level index (1-based).
        remove_deadends (bool): Whether dead ends are removed in
            generated maze.
        width (PositiveInt): Maze width in cells.
        height (PositiveInt): Maze height in cells.
        seed (int): Random seed for maze generation.
        pacgum (NonNegativeInt): Pacgum count override or placement hint.
        level_max_time (PositiveInt): Time limit for the level in seconds.
        speed_factor_player (PositiveFloat): Player movement speed factor.
        max_player_acceleration (PositiveInt): Max player acceleration cap.
        speed_factor_ghost (PositiveFloat): Ghost movement speed factor.
        bonus_fruit_type (BonusFruitType): Bonus fruit kind for the level.
        points_per_bonus_fruit (PositiveInt): Score awarded per bonus fruit.
        walls_color (tuple[int, ...]): Wall RGB color tuple.
    """

    map_filename: str = ""
    number: PositiveInt = 1
    remove_deadends: bool = True
    width: PositiveInt = 14
    height: PositiveInt = 12
    seed: int = 0
    pacgum: NonNegativeInt = 42
    level_max_time: PositiveInt = 90
    speed_factor_player: PositiveFloat = 0.01
    max_player_acceleration: PositiveInt = 5  # max_d = max(dx+dy)
    speed_factor_ghost: PositiveFloat = 0.02
    bonus_fruit_type: BonusFruitType = BonusFruitType.CHERRY
    points_per_bonus_fruit: PositiveInt = 100
    walls_color: tuple[int, ...] = (40, 200, 40)

    @property
    def size(self) -> tuple[PositiveInt, PositiveInt]:
        """Return level dimensions as (width, height)."""
        return (self.width, self.height)

    @field_validator("map_filename", mode="before")
    @classmethod
    def fix_map_filename(cls, value: Any) -> str:
        """Validate map filename."""
        if not isinstance(value, str):
            return ""
        return value

    @field_validator("bonus_fruit_type", mode="before")
    @classmethod
    def fix_BonusFruitType(cls, value: Any) -> BonusFruitType:
        """Normalize bonus fruit value to a known enum member."""
        try:
            f_name = str(value)
            fruit = BonusFruitType[f_name.upper()]
        except (KeyError, TypeError, ValueError):
            fruit = BonusFruitType.CHERRY
            print("Can't find fruit: ", value, "!")
        return fruit

    @field_validator("points_per_bonus_fruit", mode="before")
    @classmethod
    def fix_bonus_points(cls, value: Any) -> PositiveInt:
        """Validate bonus fruit score value."""
        try:
            int_val = int(value)
            if int_val < 0:
                print("Points per bonus fruit is less than 1. "
                      "Using default value (100)")
                return 1
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of points_per_bonus_fruit. "
                  "Using default value (100)")
            return 1

    @field_validator("number", mode="before")
    @classmethod
    def fix_number(cls, value: Any) -> PositiveInt:
        """Validate level number."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("Level number is less than 1. Using default value")
                return 1
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the level number. Using default value")
            return 1

    @field_validator("remove_deadends", mode="before")
    @classmethod
    def fix_is_perfect(cls, value: Any) -> bool:
        """Validate dead-end removal flag."""
        try:
            return bool(value)
        except (TypeError, ValueError):
            print("Wrong type of the 'remove_deadends' parameter."
                  " Using default value")
            return True

    @field_validator("width", mode="before")
    @classmethod
    def fix_width(cls, value: Any) -> PositiveInt:
        """Validate maze width bounds."""
        try:
            int_val = int(value)
            if int_val < 3 or int_val > 40:
                print("Width is < 3 or > 40. Using default value")
                int_val = 14
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the width. Using default value")
            return 14

    @field_validator("height", mode="before")
    @classmethod
    def fix_height(cls, value: Any) -> PositiveInt:
        """Validate maze height bounds."""
        try:
            int_val = int(value)
            if int_val < 3 or int_val > 20:
                print("Height is < 3 or > 20. Using default value")
                int_val = 12
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the height. Using default value")
            return 14

    @field_validator("seed", mode="before")
    @classmethod
    def fix_seed(cls, value: Any) -> int:
        """Validate level seed value."""
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Wrong type of the seed. Using default value")
            return 0

    @field_validator("pacgum", mode="before")
    @classmethod
    def fix_pacgum(cls, value: Any) -> NonNegativeInt:
        """Validate pacgum count value."""
        try:
            int_val = int(value)
            if int_val < 0:
                print("'pacgum' is < 0. Using default value")
                int_val = 42
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'pacgum'. Using default value")
            return 42

    @field_validator("max_player_acceleration", mode="before")
    @classmethod
    def fix_max_player_acceleration(cls, value: Any) -> PositiveInt:
        """Validate maximum player acceleration."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'max_player_acceleration' is < 1. Using default value")
                int_val = 5
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the 'max_player_acceleration'."
                  "Using default value")
            return 5

    @field_validator("level_max_time", mode="before")
    @classmethod
    def fix_level_max_time(cls, value: Any) -> PositiveInt:
        """Validate level time limit."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'level_max_time' is < 1. Using default value")
                int_val = 90
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the 'level_max_time'. Using default value")
            return 90

    @field_validator("speed_factor_player", mode="before")
    @classmethod
    def fix_speed_factor_player(cls, value: Any) -> PositiveFloat:
        """Validate player speed factor."""
        try:
            f_val = float(value)
            if f_val <= 0:
                print("'speed_factor_player' is <= 0. Using default value")
                f_val = 0.01
            return f_val
        except (TypeError, ValueError):
            print("Wrong type of the 'speed_factor_player'."
                  " Using default value")
            return 0.01

    @field_validator("speed_factor_ghost", mode="before")
    @classmethod
    def fix_speed_factor_ghost(cls, value: Any) -> PositiveFloat:
        """Validate ghost speed factor."""
        try:
            f_val = float(value)
            if f_val <= 0:
                print("'speed_factor_ghost' is <= 0. Using default value")
                f_val = 0.02
            return f_val
        except (TypeError, ValueError):
            print("Wrong type of the 'speed_factor_ghost'."
                  " Using default value")
            return 0.02

    @field_validator("walls_color", mode="before")
    @classmethod
    def fix_walls_color(cls, value: Any) -> tuple[int, ...]:
        """Validate wall color and convert to RGB tuple."""
        try:
            color = tuple(pg.Color(value)[:3])
            return color
        except (TypeError, ValueError) as ex:
            print("Wrong value for walls_collor "
                  " Using default value.", ex)
            return ((40, 200, 40))

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


class Config(BaseModel):
    """Game configuration model loaded from JSON.

    Stores global gameplay settings and normalizes invalid values through
    field validators to keep the game running with safe defaults.

    Attributes:
        highscores_filename (str): Path to the highscores JSON file.
        levels (list[Level]): Ordered level definitions.
        lives (PositiveInt): Initial number of player lives.
        points_per_pacgum (PositiveInt): Score gained per pacgum.
        points_per_super_pacgum (PositiveInt): Score gained per super pacgum.
        points_per_ghost (PositiveInt): Score gained per eaten ghost.
        seed (int): Base random seed for generation logic.
        cheat (bool): Enables evaluation cheat features when True.
        fullscreen_mode (bool): Enables fullscreen display mode when True.
    """

    default_highscores_filename: ClassVar[str] = "highscores.json"

    highscores_filename: str = default_highscores_filename
    levels: list[Level] = [Level()]
    lives: PositiveInt = 3
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False
    fullscreen_mode: bool = False

    @field_validator("highscores_filename", mode="before")
    @classmethod
    def fix_highscores_filename(cls, value: Any) -> str:
        """Validate highscores filename format."""
        if not isinstance(value, str):
            print("Wrong type of 'highscores_filename'. "
                  "Using default value:", cls.default_highscores_filename)
            return cls.default_highscores_filename
        if len(value) < 6 or not value.endswith(".json"):
            print("Wrong format of 'highscores_filename'. "
                  "Using default value:", cls.default_highscores_filename)
            return cls.default_highscores_filename
        return value

    @field_validator("levels", mode="before")
    @classmethod
    def fix_levels(cls, value: Any) -> list[Level]:
        """Validate level list input."""
        if not isinstance(value, list):
            print("Wrong type of the 'levels'. "
                  "Using default demo level settings")
            return [Level()]
        if not value:
            print("Empty 'levels'. Using default demo level settings")
            return [Level()]
        return value

    @field_validator("levels", mode="after")
    @classmethod
    def check_level_numbers(cls, value: list[Level]) -> list[Level]:
        """Validate levels list."""
        numbers: list[int] = []
        for lev in value:
            if lev.number in numbers:
                print("There are duplicate level numbers."
                      "Using default demo level settings")
                return [Level()]
            numbers.append(lev.number)
        if 1 not in numbers:
            print("There is no level number 1."
                  "Using default demo level settings")
            return [Level()]
        return value

    @field_validator("lives", mode="before")
    @classmethod
    def fix_lives(cls, value: Any) -> PositiveInt:
        """Validate initial lives count."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'lives' is < 1. Using default value")
                int_val = 3
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'lives'. Using default value")
            return 3

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def fix_points_per_pacgum(cls, value: Any) -> PositiveInt:
        """Validate pacgum score value."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'points_per_pacgum' is < 1. Using default value")
                int_val = 10
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'points_per_pacgum'. Using default value")
            return 10

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def fix_points_per_super_pacgum(cls, value: Any) -> PositiveInt:
        """Validate super pacgum score value."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'points_per_super_pacgum' is < 1. Using default value")
                int_val = 50
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'points_per_super_pacgum'."
                  " Using default value")
            return 50

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def fix_points_per_ghost(cls, value: Any) -> PositiveInt:
        """Validate ghost score value."""
        try:
            int_val = int(value)
            if int_val < 1:
                print("'points_per_ghost' is < 1. Using default value")
                int_val = 200
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'points_per_ghost'. Using default value")
            return 200

    @field_validator("seed", mode="before")
    @classmethod
    def fix_seed(cls, value: Any) -> int:
        """Validate random seed value."""
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Wrong type of 'seed'. Using default value")
            return 0

    @field_validator("cheat", mode="before")
    @classmethod
    def fix_cheat(cls, value: Any) -> bool:
        """Validate cheat mode flag."""
        try:
            return bool(value)
        except (TypeError, ValueError) as er:
            print("Wrong type of 'cheat'. Using default value.\n", er)
            return False

    @field_validator("fullscreen_mode", mode="before")
    @classmethod
    def fix_fullscreen_mode(cls, value: Any) -> bool:
        """Validate fullscreen mode flag."""
        try:
            return bool(value)
        except (TypeError, ValueError) as er:
            print("Wrong type of 'fullscreen_mode'."
                  "Using default value.\n", er)
            return False

    def print(self) -> None:
        print("--Config:")
        print("Seed:", self.seed)
        print("Cheat:", self.cheat)
        print("Levels: ", len(self.levels))
        for l_ in self.levels:
            l_.print()
