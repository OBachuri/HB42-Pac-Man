*This project has been created as part of the 42 curriculum by obachuri and iiunusov*

---

# Pac-Man 42

This project is part of the 42.fr curriculum.

The task: Recreate the famous arcade game Pac-man!

- Use external library for maze generation (‘A-Maze-ing‘ package from other "42" people)
- Pac-Man starts from the center of the maze.
- One ghost appear in each corner of the maze.


## Game screen example
![Result](result.png)


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

- **W** or **⇧** - Move Up
- **A** or **⇦** - Move Left
- **S** or **⇩** - Move Down
- **D** or **⇨** - Move Right
- **Space** - Stop
- **Esc** - Pause / Exit game

#### Cheat mode

If you started game with ``` "cheat":  true ``` in config.json - for you available the following additional options:
- **1** - Invincibility (no life lost; ghosts cannot eat the player).
- **2** - Level skip (immediately win the current level).
- **3** - Ghost freeze (ghosts stop moving).
- **4** - Extra lives (add extra lives to the player).
- **5** - Increased speed (player moves faster).
- **6** - Decreased speed (player moves slower).
- **7** - Change ghost mode.
- **F** - Ghosts SCATTER


### Configuration File

The configuration file controls the maze generation physics and rules.

```json
{
"highscore_filename": "pc_score.json",
"lives": 3,
"points_per_pacgum" : 10,
"points_per_super_pacgum" : 50,
"points_per_ghost" : 200,
"cheat": true,
"levels": [
	{
	"number": 1,
	"width": 14,
	"height": 10,
	"pacgum" : 42,
	"seed": 42,
	"level_max_time": 130,
	"bonus_fruit_type": "Strawberry",
	"points_per_bonus_fruit": 300,
	"remove_deadends": true,
	"speed_factor_ghost": 0.04,
	"max_player_acceleration": 6
	},
	{
	"number": 100,
	"map_filename": "inc/maps/maze-3.txt"
	}
	]
}
```

## Requirements

- Python 3.10 or later
- Pygame
- Pydantic
- Pip (for install)

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
- Maze creating and drawing
- Pac-Man's movements and animation

IIunusov:
- Project management
- Main menu
- Highscore system
- Parsing and error handling
- Ghost movement algorithm 

## License

Part of the 42 curriculum project.
