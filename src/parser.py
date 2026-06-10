import json
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError, PositiveInt
from typing import List, Dict, Any

class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    level: List[Dict[str, Any]]
    lives: PositiveInt = 3
    pacgum: PositiveInt = 42
    points_per_pacgum: PositiveInt = 10
    points_per_super_pacgum: PositiveInt = 50
    points_per_ghost: PositiveInt = 200
    seed: int = 42
    level_max_time: PositiveInt = 90
    cheat: bool = False


class Parser:
    @staticmethod
    def delete_comments(text: List[str]) -> List[str]:
        return [line for line in text if not line.strip().startswith("#")]
        # for line in text:
        #     if not line.strip().startswith("#"):
        #         result.append(line)

    @classmethod
    def get_config_data(cls, path: str) -> Dict[str, Any]:
        cfg_data: Dict[str, Any] = {}
        with open(path) as f:
            raw_text = f.readlines()
            clean_json = cls.delete_comments(raw_text)
            try:
                cfg_data = json.loads("".join(clean_json))
            except json.JSONDecodeError as e:
                print("Got JSON decoding error:", e)
        return cfg_data
    
    @classmethod
    def get_config(cls, path: str) -> Config:
        cfg_data = cls.get_config_data(path)

        if not cfg_data:
            print("Could not fetch config data")
            return None

        try:
            config = Config.model_validate(cfg_data)
            return config
        except ValidationError as e:
            print(f"Got an error:", e)



