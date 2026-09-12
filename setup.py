"""Helper script to setup dependencies layer required for the sudoku games."""

import argparse
import os
import subprocess
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_REQUIREMENTS_PATH = os.path.join(MODULE_DIR, "dev_requirements.txt")
SUDOKU_GUI_MODULE_DIR = os.path.join(MODULE_DIR, "SudokuGame")
SUDOKU_TERMINAL_MODULE_DIR = os.path.join(MODULE_DIR, "SudokuTerminal")

SUDOKU_GUI_REQUIREMENTS_PATH = os.path.join(SUDOKU_GUI_MODULE_DIR, "requirements.txt")
SUDOKU_TERMINAL_REQUIREMENTS_PATH = os.path.join(SUDOKU_TERMINAL_MODULE_DIR, "requirements.txt")


def get_python_binary_path(virtual_env_dir: str | None = None):
    if virtual_env_dir is None or not is_virtual_environment(virtual_env_dir):
        return "python3" if os.name == "posix" else "python"

    virtual_env_python_binary_path = os.path.join(
        "bin" if os.name == "posix" else "Scripts", "python.exe"
    )
    return os.path.join(virtual_env_dir, virtual_env_python_binary_path)


def installer(
    virtual_env_dir: str | None = None,
    upgrade_pip: bool = True,
    install_terminal_requirements: bool = True,
    install_gui_requirements: bool = True,
    install_dev_dependencies: bool = False,
) -> None:
    """Installs sudoku dependencies.

    Parameters
    ----------
    - virtual_env_dir:
        Optional path of virtual environment. If it is a falsely value,
        it will not be used.
    """

    virtual_env_dir = virtual_env_dir or ""
    if not virtual_env_dir:
        virtual_env_dir = ""

    python_path = get_python_binary_path(virtual_env_dir)
    if upgrade_pip is True:
        print("Upgrading pip........")
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"])
        print()

    if install_terminal_requirements is True:
        print("Installing sudoku terminal game requirements............")
        subprocess.run(
            [python_path, "-m", "pip", "install", "-r", SUDOKU_TERMINAL_REQUIREMENTS_PATH]
        )
        print()

    if install_gui_requirements is True:
        print("Installing sudoku gui game requirements..............")
        subprocess.run([python_path, "-m", "pip", "install", "-r", SUDOKU_GUI_REQUIREMENTS_PATH])
        print()

    if install_dev_dependencies is True:
        print("Installing optional dev dependencies...............")
        subprocess.run([python_path, "-m", "pip", "install", "-r", DEV_REQUIREMENTS_PATH])
        print()


def is_virtual_environment(virtual_env_dir: str) -> bool:
    """Check whether provided path is a valid python virtual environment directory."""

    return os.path.exists(os.path.join(virtual_env_dir, "pyvenv.cfg")) and (
        os.path.exists(
            os.path.join(virtual_env_dir, "bin", "python")
            if os.name == "posix"
            else os.path.join(virtual_env_dir, "Scripts", "python.exe")
        )
    )


def is_running_virtual_environment() -> bool:
    """Check whether program is running in a virtual environment.

    References
    ----------
    - https://stackoverflow.com/questions/1871549#answer-1883251
    """

    base_prefix = (
        getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    )
    return sys.prefix != base_prefix


def _print_successful_virtual_environment_setup_message(env_path: str) -> None:
    """Prints virtual environment setup message after successful setup."""

    print(
        f"\nSetup new virtual environment {env_path}. Use the `"
        + (
            os.path.join(env_path, "Scripts", "activate")
            if os.name == "nt"
            else "source " + os.path.join(env_path, "bin", "activate")
        )
        + "` command to activate virtual environment\n"
    )


def setup_virtual_environment(env_dir: str = MODULE_DIR, env_name: str = "venv") -> str:
    """
    Create a virtual environment in the specified environment directory
    (by default, it is the dirpath of the script where this function exists).

    Ensure that virtualenv is installed before attempting this.

    Returns
    -------
    - path: Path of the newly created virtual environment.

    Raises
    ------
    - RuntimeError: Raised when failed to initialize virtual environment.
    """

    path = os.path.join(env_dir, env_name)
    try:
        subprocess.run(
            [
                "python" if os.name == "nt" else "python3",
                "-m",
                "venv",
                path,
            ]
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to initialize virtual environment. "
            f"Ensure virtualenv is installed. Error raised: {repr(exc)}"
        )

    _print_successful_virtual_environment_setup_message(env_path=path)
    return path


class PathDoesNotExistError(FileNotFoundError):
    """Custom Exception Defined to handle path not existing errors"""

    def __init__(self, *args, path=None, **kwargs):
        msg = "Provided path does not exist"
        if path is not None:
            msg += f": {path}"
        super().__init__(msg, *args, **kwargs)


class CheckPathExistsAction(argparse.Action):
    """Custom argparse Action to validate path variables.

    It will basically check if the path exists or not.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        path_to_check = values
        if not os.path.exists(path_to_check):
            raise PathDoesNotExistError(path=path_to_check)
        setattr(namespace, self.dest, values)


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sudoku_game_installer",
        description="Installs dependencies required for running the sudoku games",
    )

    parser.add_argument(
        "--upgrade-pip",
        type=bool,
        default=True,
        required=False,
        help="Set whether pip should be upgraded",
    )
    parser.add_argument(
        "--global",
        dest="is_global",
        type=bool,
        default=False,
        required=False,
        help="Set whether required dependencies should be installed globally or not. "
        "This avoids the creation of a virtual environment. However, it is recommended "
        "to use a virtual environment to ensure no system breaking dependencies are installed.",
    )
    parser.add_argument(
        "--env-dir",
        type=str,
        action=CheckPathExistsAction,
        default=MODULE_DIR,
        required=False,
        help="Path where the virtual environment will be created. ",
    )
    parser.add_argument(
        "--env-name",
        type=str,
        default="venv",
        required=False,
        help="Name of the virtual environment to set.",
    )
    parser.add_argument(
        "--install-gui-requirements",
        type=bool,
        default=True,
        required=False,
        help="Set whether the dependencies for the Sudoku GUI game should be installed.",
    )
    parser.add_argument(
        "--install-terminal-requirements",
        type=bool,
        default=True,
        required=False,
        help="Set whether the dependencies for the Sudoku Terminal game should be installed.",
    )
    parser.add_argument(
        "--install-dev-dependencies",
        type=bool,
        default=False,
        required=False,
        help="Set whether optional developer dependencies should "
        "be installed, which can be used for developing this project.",
    )

    args = parser.parse_args()
    return args


def main():
    args = get_arguments()

    install_global: bool = args.is_global
    virtual_env_dir: str = os.path.join(args.env_dir, args.env_name)
    if (
        not is_running_virtual_environment() or not is_virtual_environment(virtual_env_dir)
    ) and install_global is False:
        virtual_env_dir = setup_virtual_environment(env_dir=args.env_dir, env_name=args.env_name)

    print("Running installation......")
    installer(
        virtual_env_dir=virtual_env_dir,
        upgrade_pip=args.upgrade_pip,
        install_gui_requirements=args.install_gui_requirements,
        install_terminal_requirements=args.install_terminal_requirements,
        install_dev_dependencies=args.install_dev_dependencies,
    )
    _print_successful_virtual_environment_setup_message(env_path=virtual_env_dir)


if __name__ == "__main__":
    main()
