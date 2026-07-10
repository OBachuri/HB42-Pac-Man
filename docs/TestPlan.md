
## PacMan-42 - Acceptance Test Plan


| ID    | Requirement              | Test Procedure                             | Expected Result                                      | Pass/Fail |
| ----- | ------------------------ | ------------------------------------------ | ---------------------------------------------------- | --------- |
| AT-01 | Game starts correctly    | Launch the game                            | Main menu is displayed without errors                |Pass|
| AT-02 | Random maze generation   | Start a new game five times                | A different valid maze is generated each time        |Pass|
| AT-03 | Maze size selection      | Select different maze sizes (8×8 to 20×20) | Maze matches the selected size                       |Pass|
| AT-04 | Pac-Man movement         | Move Pac-Man using the keyboard            | Pac-Man moves smoothly and cannot pass through walls |Pass|
| AT-05 | Pellet collection        | Eat a pellet                               | Pellet disappears and score increases by 10          |Pass|
| AT-06 | Power pellet             | Eat a power pellet                         | Ghosts enter frightened mode                         |Pass|
| AT-07 | Ghost AI                 | Observe ghost behavior                     | Ghosts actively pursue Pac-Man through the maze      |Pass|
| AT-08 | Ghost collision          | Allow a ghost to touch Pac-Man             | Pac-Man loses one life                               |Pass|
| AT-09 | Eating frightened ghosts | Eat a frightened ghost                     | Ghost returns to its home and score increases        |Pass|
| AT-10 | Bonus fruit              | Collect enough pellets to spawn a fruit    | Fruit appears and awards the correct points          |Pass|
| AT-11 | Level completion         | Eat all pellets                            | Next level begins with a newly generated maze        |Pass|
| AT-12 | Game over                | Lose all lives                             | Game Over screen is displayed                        |Pass|
| AT-13 | Sound effects            | Trigger game events                        | Appropriate sound effects are played                 |Pass|
| AT-14 | High-score saving        | Finish a game with a high score            | Score is stored and displayed on the next launch     |Pass|
| AT-15 | Performance              | Play for at least 10 minutes               | Game remains responsive (≈60 FPS) without crashes    |Pass|
