"""Script to launch a sudoku game."""

import argparse
import importlib

GAME_CHOICES = ("terminal", "gui")
DEFAULT_SUDOKU_GUI_MODULE = "SudokuGame.player"
DEFAULT_SUDOKU_GUI_RUNNER = "main"
DEFAULT_SUDOKU_TERMINAL_MODULE = "SudokuTerminal.sudokuPlayer"
DEFAULT_SUDOKU_TERMINAL_RUNNER = "main"


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sudoku_game_launcher",
        description="Interactive launcher that can be used to start a sudoku game",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "game",
        nargs="?",
        type=str,
        choices=GAME_CHOICES,
        help="Specify the sudoku game type to run.",
    )
    group.add_argument(
        "--game-type",
        type=str,
        choices=GAME_CHOICES,
        required=False,
        help="Specify the sudoku game type to run.",
    )

    parser.add_argument(
        "--sudoku-gui-module",
        type=str,
        default=DEFAULT_SUDOKU_GUI_MODULE,
        required=False,
        help="Module where the sudoku gui game exists",
    )
    parser.add_argument(
        "--sudoku-gui-runner",
        type=str,
        default=DEFAULT_SUDOKU_GUI_RUNNER,
        required=False,
        help="Function defined in the sudoku gui module that is used to run the sudoku gui game",
    )
    parser.add_argument(
        "--sudoku-terminal-module",
        type=str,
        default=DEFAULT_SUDOKU_TERMINAL_MODULE,
        required=False,
        help="Module where the sudoku terminal game exists",
    )
    parser.add_argument(
        "--sudoku-terminal-runner",
        type=str,
        default=DEFAULT_SUDOKU_TERMINAL_RUNNER,
        required=False,
        help="Function defined in the sudoku terminal module that "
        "is used to run the sudoku terminal game",
    )

    args = parser.parse_args()
    return args


def start_sudoku_game(module: str, runner: str, *args, **kwargs):
    """Starts game with the specified module and runner.

    Any additional arguments are passed directly to the runner function.
    """

    provided_module = importlib.import_module(module)
    game_runner = getattr(provided_module, runner)

    print("Starting sudoku game.....")
    game_runner(*args, **kwargs)


def main():
    arguments = get_arguments()
    game = arguments.game or arguments.game_type

    start_sudoku_game(
        module=getattr(arguments, f"sudoku_{game}_module"),
        runner=getattr(arguments, f"sudoku_{game}_runner"),
    )


if __name__ == "__main__":
    main()
