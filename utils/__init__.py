from .abstract import SudokuAbstract
from .custom_types import GRID_TYPE
from .exceptions import InvalidSudokuError, MissingSudokuClassError, NotSquareArrayError
from .sudoku import SquareSudoku, SudokuBacktracking

Sudoku: type[SudokuAbstract] = SquareSudoku

__all__ = [
    "GRID_TYPE",
    "InvalidSudokuError",
    "MissingSudokuClassError",
    "NotSquareArrayError",
    "SudokuAbstract",
    "SquareSudoku",
    "SudokuBacktracking",
    "Sudoku",
]

try:
    from .csudoku import CSudoku
except ModuleNotFoundError:
    pass
else:
    Sudoku = CSudoku

    __all__.append("CSudoku")
