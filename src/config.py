from pydantic import BaseModel, Field
from pydantic import PositiveInt, NonNegativeInt, PositiveFloat


class Level(BaseModel):
    map_filename: str = Field(min_length=1, default="")
    number: PositiveInt
    is_perfect: bool = False
    width: int = Field(ge=3, default=14)
    height: int = Field(ge=3, default=12)
    seed: int = 42
    level_max_time: PositiveInt = 90
    speed_factor_player: PositiveFloat = 0.01
    speed_factor_ghost: PositiveFloat = 0.02

    @property
    def size(self) -> tuple[PositiveInt, PositiveInt]:
        return (self.width, self.height)


class Config(BaseModel):
    highscores_filename: str = Field(min_length=6, default="highscores.json")
    levels: list[Level]
    lives: PositiveInt = 3
    pacgum: NonNegativeInt = 42
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False
