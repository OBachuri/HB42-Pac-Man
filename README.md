*This project has been created as part of the 42 curriculum by obachuri and ......*

---

# Pac-Man

This project is part of the 42.fr curriculum.

The task: Recreate the famous arcade game Pac-man!

- Use external library for maze generation (‘A-Maze-ing‘ package from other "42" piople)

> [!WARNING]
> The program does not ready. It is under development now.

## Installation

```bash
make install
```

## Usage

```bash
# Run with default configuration
make run

# Run with your configuration
make run my_config.json

# Run directly with Python
python3 pac-man.py my_config.json
```

## Play

### Controls

- **W** - Move Up
- **A** - Move Left
- **S** - Move Down
- **D** - Move Right
- **Space** - Stop
- **Esc** - Exit game


### Configuration File

The configuration file controls the maze generation physics and rules.

```json
{
"highscore_filename": "pc_score.json",
"level": ["Level 1","Level 2","Level 3"],
"width": [22,25,30],
"height": [15,18,20],
"lives": 3,
"pacgum" : 42,
"points_per_pacgum" : 10,
"points_per_super_pacgum" : 50,
"points_per_ghost" : 200,
"seed" : 42,
"level_max_time" : 90
}
```

## Requirements

- Python 3.10 or later
- Pygame
- Pydantic
- Dotenv


## Resources

Pac-Man on WiKi 
https://en.wikipedia.org/wiki/Pac-Man

PGame - RPG example
https://www.youtube.com/watch?v=ECqUrT7IdqQ&list=PLi77irUVkDatlbulEY4Kz8O107HO8RGH8

Pacmancode - How to program a Pacman game in the Python language using Pygame
https://pacmancode.com/

Resources DFS 
https://en.wikipedia.org/wiki/Depth-first_search

Resources PRIMS
https://en.wikipedia.org/wiki/Prim%27s_algorithm


### Team Project Management

Team Members

Obachuri
- Project lead
- Main architecture design

## License

Part of the 42 curriculum project.
