*This project has been created as part of the 42 curriculum by obachuri and iiunusov*

---

# Pac-Man 42

## Description

This project is a Python implementation of the classic arcade game Pac-Man, developed with an object-oriented and modular architecture.  
The project focuses on gameplay completeness, robustness, and maintainability:

- Playable multi-level Pac-Man loop
- Configurable game behavior via JSON config file
- Persistent top-10 highscores
- Integration of an external A-Maze-ing maze generator package
- Menu/game over/victory UI flow
- Cheat mode for peer-evaluation convenience
- Packaging-ready project with Makefile automation

Main game loop:

`Main Menu → Start Game → Win/Lose → Enter Name (save highscore) → Back to Main Menu`

---

## Game screen example
![Result](result.png)

## [Play the web version](https://obachuriiiunusov.itch.io/pacman42)


## Instructions

### Requirements

- Python 3.10 or later
- Pygame
- Pydantic
- Pip (for install)


### Installation

```bash
make install
```
This target creates/uses `.venv` and installs dependencies (including `pygame-ce`, `pydantic`, maze generator wheel, linting tools, etc.).

### Usage

```bash
# Run with default configuration
make run

# Run with your configuration
make run my_config.json

# Run directly with Python
python3 pac-man.py my_config.json
```

### Debug

```bash
make debug config.json
```

### Lint

```bash
make lint
```
Optional stricter check:

```bash
make lint-strict
```

## Play

### Controls

- **W** or **⇧** - Move Up
- **A** or **⇦** - Move Left
- **S** or **⇩** - Move Down
- **D** or **⇨** - Move Right
- **Space** - Stop
- **Esc** - Pause / Exit game
- **F11** - Full screan 

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


### Configuration

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
	"max_player_acceleration": 6,
	"walls_color": "#1e2ac9"
	},
	{
	"number": 100,
	"map_filename": "inc/maps/maze.txt"
	}
	]
}
```
#### Key notes

- Unknown keys are ignored.
- Missing/invalid values are replaced with safe defaults where applicable.
- Typical tunables:
  - player lives
  - scoring values
  - level dimensions and timers
  - random seed
  - cheat mode
  - highscore output file path/name

---
## Highscore

The project uses a persistent highscore system stored in JSON (`highscores_filename` from config, default `highscores.json`).

### Behavior

- Highscores are loaded at game start.
- At game end (win or lose), player decides to quit or to store their score. If yes, player enters a name and score is stored.
- Name rules:
  - max 10 characters
  - alphanumeric + spaces
- Score rules:
  - non-negative integer
- Top 10 entries are kept and saved to disk.

---
## Maze Generation

This project integrates an **assigned external A-Maze-ing package** (not authored in this repository) through a dedicated adapter/loader workflow.

### Integration principles

- The external package is used **as-is**.
- Loader adapts to package API (not the other way around).
- Maze generation failures are handled gracefully with explicit error messages.
- `PERFECT = False` is expected for Pac-Man-friendly corridor topology, according to subject constraints.

The entrypoint imports maze generation package at runtime and exits with a clear message if unavailable.

---
## Implementation 

### Implementation technical summary
- Entry point: `pac-man.py`
- Runtime flow:
  1. Dependency checks (`pygame`, `pydantic`, maze package)
  2. Config parsing/validation
  3. App initialization
  4. Async game loop execution
- Core design goals:
  - no hard crashes on expected faulty inputs
  - modular code organization under `src/`
  - separation of concerns (parsing/config/game/ui/storage)

### Key design decisions
- Maze for level can be randomly generated or read from file, there is function to delete one random wall for all dead ends in a maze.
- Movement - PacMan move not only by grid lines but in any direction inside free space with acceleration. Ghosts - only Grid-based movement with constant speed.
- Ghost AI - here is several modes:
  - Chase - When the ghosts chase Pac-Man, each of them uses a unique strategy, almost as in the original game:
    - Red ghost (Blinky, Shadow) - always runs toward PacMan's current position via the shortest path.
    - Pink ghost (Speedy) - He targets the point located four tiles ahead of Pac-Man.
    - Cyan ghost (Inky, Bashful) - Target tile by doubling a vector drawn from the Red ghost to a point two tiles ahead of PacMan
    - Orange ghost (Clyde, Pockey) - Target a random cell at a specific distance (3 tiles) from Pac-Man.
  - Scatter - All ghosts run to their corner
  - Frightened ghosts change direction immediately and then randomly choose direction but not run back if it possible. 

- Rendering - The maze is pre-rendered onto the surface for rapid copying (blitting), while the dots, Pac-Man, and the ghosts are drawn in every frame.

---

## General Software Architecture

High-level architecture (actual class names may evolve):

- **Entrypoint Layer**
  - `pac-man.py`: bootstrap, dependency checks, CLI config argument, app launch
- **Configuration Layer**
  - Parser module (`pc_parser`) for config loading and validation
  - Config model (`config`) with typed fields/default logic
- **Application Layer**
  - App orchestrator (`pc_app`) managing screen flow/game lifecycle
- **Domain/Game Layer**
  - level state, entities (player, ghosts, pellets), scoring, timer logic
- **UI Layer**
  - main menu, in-game HUD, pause, game over, victory, highscores, instructions
- **Persistence Layer**
  - highscores JSON read/write with robust file error handling
- **Integration Layer**
  - adapter usage of external `mazegenerator` package

This modular decomposition supports reuse, easier testing, and clearer maintenance boundaries.

---

## Project Management

The responsibilities were distributed among the team members as follows:

*Obachuri*:
- Main architecture design
- Maze creating and drawing
- Pac-Man's movements and animation

*IIunusov*:
- Project management
- Main menu
- Highscore system
- Parsing and error handling
- Ghost movement algorithm 

Project management artifacts are maintained in a dedicated directory in the repository (timeline, tracking, risk analysis, role distribution, testing/acceptance notes, blockers/conflicts summary).

See the [project-management folder for evidence and supporting documents.](docs/)

---
## Resources

[Pac-Man on WiKi](https://en.wikipedia.org/wiki/Pac-Man)  
[Pac-Man Ghosts Wiki](https://en.wikipedia.org/wiki/Ghosts_(Pac-Man))  
[PyGame Docs](https://www.pygame.org/docs/)  
[PyGame - RPG example](https://www.youtube.com/watch?v=ECqUrT7IdqQ&list=PLi77irUVkDatlbulEY4Kz8O107HO8RGH8)  
[Pacmancode - How to program a Pacman game in the Python language using Pygame](https://pacmancode.com/)  
[Resources DFS](https://en.wikipedia.org/wiki/Depth-first_search)  
[Resources PRIMS](https://en.wikipedia.org/wiki/Prim%27s_algorithm)

### AI Usage

Tools Used:
- ChatGPT (GPT-4)
- Nano Banana 2

AI was used to generate images and structuring this README.  

## License

Part of the 42 curriculum project.
