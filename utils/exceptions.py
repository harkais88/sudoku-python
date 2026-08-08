"""Custom Exceptions defined for the Sudoku Codebase"""


class MissingSudokuClassError(AttributeError):
    """Exception raised if the Sudoku class was not found in expected module"""

    pass


class NotSquareArrayError(ValueError):
    """Exception raised when array is not a square array"""

    pass


class InvalidSudokuError(ValueError):
    """Exception raised when array is not a valid sudoku"""

    pass


class NumberOfSymbolsAlreadySet(ValueError):
    """Exception raised when the number of symbols is attempted to be reset"""

    pass
