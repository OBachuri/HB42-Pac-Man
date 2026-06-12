from pydantic import BaseModel, Field
from pydantic import PositiveInt, NonNegativeInt, PositiveFloat, field_validator


class Level(BaseModel):
    map_filename: str = ""
    number: PositiveInt = 1
    is_perfect: bool = False
    width: PositiveInt = 14
    height: PositiveInt = 12
    seed: int = 0
    level_max_time: PositiveInt = 90
    speed_factor_player: PositiveFloat = 0.01
    speed_factor_ghost: PositiveFloat = 0.02

    @property
    def size(self) -> tuple[PositiveInt, PositiveInt]:
        return (self.width, self.height)
    
    @field_validator("number", mode="before")
    @classmethod
    def fix_number(cls, value) -> int:
        try:
            int_val = int(value)
            if int_val < 1:
                print("Level number is less than 1. Using default value")
                return 1
            return int_val
        except (TypeError, ValueError):
            print("Wrong type of the level number. Using default value")
            return 1
        
    @field_validator("is_perfect", mode="before")
    @classmethod
    def fix_is_perfect(cls, value) -> bool:
        try:
            return bool(value)
        except (TypeError, ValueError):
            print("Wrong type of the 'is_perfect' parameter. Using default value")
            return False
        
    @field_validator("width", mode="before")
    @classmethod
    def fix_width(cls, value) -> bool:
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
    def fix_height(cls, value) -> bool:
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
    def fix_seed(cls, value) -> bool:
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Wrong type of the seed. Using default value")
            return 0
        
    @field_validator("level_max_time", mode="before")
    @classmethod
    def fix_level_max_time(cls, value) -> bool:
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
    def fix_speed_factor_player(cls, value) -> PositiveFloat:
        try:
            f_val = PositiveFloat(value)
            if f_val <= 0:
                print("'speed_factor_player' is <= 0. Using default value")
                f_val = 0.01
            return f_val
        except (TypeError, ValueError):
            print("Wrong type of the 'speed_factor_player'. Using default value")
            return 0.01
        
    @field_validator("speed_factor_ghost", mode="before")
    @classmethod
    def fix_speed_factor_ghost(cls, value) -> PositiveFloat:
        try:
            f_val = PositiveFloat(value)
            if f_val <= 0:
                print("'speed_factor_ghost' is <= 0. Using default value")
                f_val = 0.02
            return f_val
        except (TypeError, ValueError):
            print("Wrong type of the 'speed_factor_ghost'. Using default value")
            return 0.02


class Config(BaseModel):
    highscores_filename: str = Field(min_length=6, default="highscores.json")
    levels: list[Level] = [Level()]
    lives: PositiveInt = 3
    pacgum: NonNegativeInt = 42
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False

    @field_validator("levels", mode="before")
    @classmethod
    def fix_levels(cls, value) -> PositiveFloat:
        # try:
        #     f_val = PositiveFloat(value)
        #     if f_val <= 0:
        #         print("'speed_factor_ghost' is <= 0. Using default value")
        #         f_val = 0.02
        #     return f_val
        # except (TypeError, ValueError):
        if not isinstance(value, list):
            print("Wrong type of the 'levels'. Using default demo level settings")
            return [Level()]
        if not value:
            print("Empty 'levels'. Using default demo level settings")
            return [Level()]
        if not all([1 if Level(**level) else 0 for level in value]):
            print("Wrong type of a level in 'levels'. Using default demo level settings")
            return [Level()]
