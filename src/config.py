from typing import ClassVar, Any
from pydantic import BaseModel
from pydantic import PositiveInt, NonNegativeInt, PositiveFloat
from pydantic import field_validator


class Level(BaseModel):
    map_filename: str = ""
    number: PositiveInt = 1
    remove_deadends: bool = True
    width: PositiveInt = 14
    height: PositiveInt = 12
    seed: int = 0
    pacgum: NonNegativeInt = 42
    level_max_time: PositiveInt = 90
    speed_factor_player: PositiveFloat = 0.01
    speed_factor_ghost: PositiveFloat = 0.02

    @property
    def size(self) -> tuple[PositiveInt, PositiveInt]:
        return (self.width, self.height)

    @field_validator("number", mode="before")
    @classmethod
    def fix_number(cls, value: Any) -> PositiveInt:
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
        try:
            return bool(value)
        except (TypeError, ValueError):
            print("Wrong type of the 'remove_deadends' parameter."
                  " Using default value")
            return True

    @field_validator("width", mode="before")
    @classmethod
    def fix_width(cls, value: Any) -> PositiveInt:
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
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Wrong type of the seed. Using default value")
            return 0

    @field_validator("pacgum", mode="before")
    @classmethod
    def fix_pacgum(cls, value: Any) -> NonNegativeInt:
        try:
            int_val = int(value)
            if int_val < 0:
                print("'pacgum' is < 0. Using default value")
                int_val = 42
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of 'pacgum'. Using default value")
            return 42

    @field_validator("level_max_time", mode="before")
    @classmethod
    def fix_level_max_time(cls, value: Any) -> PositiveInt:
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

    def print(self):
        print("--Level:")
        print("Number:", self.number)
        print("Width:", self.width)
        print("Height:", self.height)
        print("Map File:", self.map_filename)
        print("Seed:", self.seed)
        print("Remove deadends:", self.remove_deadends)
        print("Time max:", self.level_max_time, "s")


class Config(BaseModel):
    default_highscores_filename: ClassVar[str] = "highscores.json"

    highscores_filename: str = default_highscores_filename
    levels: list[Level] = [Level()]
    lives: PositiveInt = 3
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False

    @field_validator("highscores_filename", mode="before")
    @classmethod
    def fix_highscores_filename(cls, value: Any) -> str:
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
        if not isinstance(value, list):
            print("Wrong type of the 'levels'. "
                  "Using default demo level settings")
            return [Level()]
        if not value:
            print("Empty 'levels'. Using default demo level settings")
            return [Level()]
        return value

    @field_validator("lives", mode="before")
    @classmethod
    def fix_lives(cls, value: Any) -> PositiveInt:
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
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Wrong type of 'seed'. Using default value")
            return 0

    @field_validator("cheat", mode="before")
    @classmethod
    def fix_cheat(cls, value: Any) -> bool:
        try:
            return bool(value)
        except (TypeError, ValueError):
            print("Wrong type of 'cheat'. Using default value")
            return False

    def print(self):
        print("--Config:")
        print("Seed:", self.seed)
        print("Cheat:", self.cheat)
        print("Levels: ", len(self.levels))
        for l_ in self.levels:
            l_.print()
