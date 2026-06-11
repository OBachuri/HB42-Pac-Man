import sys
import json
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError, Field
from pydantic import PositiveInt, NonNegativeInt


class Level(BaseModel):
    number: PositiveInt
    width: PositiveInt = 14
    height: PositiveInt = 12
    seed: int = 42
    level_max_time: PositiveInt = 90


class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    level: List[Level]
    lives: PositiveInt = 3
    pacgum: NonNegativeInt = 42
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    cheat: bool = False


class Parser:
    @classmethod
    def _get_config_data(cls, path: str) -> Dict[str, Any]:
        try:
            with open(path) as f:
                raw_text = f.readlines()
                clean_json = [line for line in raw_text
                            if not line.strip().startswith("#")]
                return json.loads("".join(clean_json))
        except json.JSONDecodeError as e:
            print("\nGot JSON decoding error:", e)
        except FileNotFoundError as e:
            print(f"\nConfig file not found: {path}")
        sys.exit(1)
    
    @classmethod
    def get_config(cls, path: str) -> Config:
        cfg_data = cls._get_config_data(path)

        try:
            return Config.model_validate(cfg_data)
        except ValidationError as e:
            print(f"\nGot an error:", e)
            sys.exit(1)
