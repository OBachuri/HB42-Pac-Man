*This project has been created as part of the 42 curriculum by obachuri and ......*

---

# Pac-Man

This project is part of the 42.fr curriculum.

The task: Recreate the famous arcade game Pac-man!

- Use external library for maze generation (‘A-Maze-ing‘ package from other "42" piople)
- Pac-Man starts from the center of the maze.
- One ghost appear in each corner of the maze.

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

#### Cheat mode

- **F** - Ghosts SCATTER

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
- Pip (for instaqll script)

## Resources

Pac-Man on WiKi: 
https://en.wikipedia.org/wiki/Pac-Man

Pac-Man Ghosts Wiki:
https://en.wikipedia.org/wiki/Ghosts_(Pac-Man)

PyGame:
https://www.pygame.org/docs/

PyGame - RPG example:
https://www.youtube.com/watch?v=ECqUrT7IdqQ&list=PLi77irUVkDatlbulEY4Kz8O107HO8RGH8

Pacmancode - How to program a Pacman game in the Python language using Pygame:
https://pacmancode.com/

Resources DFS: 
https://en.wikipedia.org/wiki/Depth-first_search

Resources PRIMS:
https://en.wikipedia.org/wiki/Prim%27s_algorithm

### AI Usage

Tools Used:
- ChatGPT (GPT-4)
- Nano Banana 2

AI was used to generate images and structuring this README.

## Project Management

Team Members

Obachuri:
- Main architecture design
- Pac-Man's movements and animation

## License

Part of the 42 curriculum project.
