import sys
import os
import asyncio


def main() -> int:
    """Run the game entrypoint.

    Initializes dependencies, loads configuration, starts the app loop,
    and exits with a process status code.

    Returns:
        int: Exit status code (0 on success).
    """

    global MazeGenerator
    global pg
    global pd

    try:
        import pygame as pg
        import pydantic as pd
    except ModuleNotFoundError as e:
        print("\nError: One of the dependencies is missing\n", e)
        print("Please run 'make install'")
        sys.exit(1)

    path_to_src = os.path.join(os.path.dirname(__file__), 'src')
    # print("="*30, path_to_src)
    sys.path.append(path_to_src)

    from src.pc_parser import Parser
    from src.config import Config
    from src.pc_app import App

    # try shcool maze generator
    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except Exception as err_msg:
        print("Error with mazegen library connection:", err_msg)
        print("Check for the presence of the package " +
              "and run 'make install' again.")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("\nError: Invalid program launch format" +
              "\nUsage 'python3 pac-man.py <config-file.json>'")
        # sys.exit(1)

    if len(sys.argv) > 1:
        config: Config = Parser.get_config(sys.argv[1])
    else:
        config = Parser.get_config()

    if config.cheat:
        config.print()

    app = App(config)
    # Run the async loop
    asyncio.run(app.run())

    return (0)


if __name__ == "__main__":
    main()
