from typing import List, Tuple
from pydantic import BaseModel, Field
from pydantic import PositiveInt, NonNegativeInt


class Level(BaseModel):
    number: PositiveInt
    width: PositiveInt = 14
    height: PositiveInt = 12
    seed: int = 42
    level_max_time: PositiveInt = 90

    @property
    def size(self) -> Tuple[PositiveInt, PositiveInt]:
        return (self.width, self.height)


class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    levels: List[Level]
    lives: PositiveInt = 3
    pacgum: NonNegativeInt = 42
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False
