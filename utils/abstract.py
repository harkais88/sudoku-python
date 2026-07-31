"""Contains abstract classes that can be used for building Sudoku classes."""

import itertools
import math
from typing import Any, Optional, Sequence

from .custom_types import GRID_TYPE
from .exceptions import InvalidSudokuError, NotSquareArrayError


class SudokuAbstract:
    """Abstract class that can be used for defining Sudoku generator classes."""

    def __init__(
        self,
        number_of_symbols: int = 9,
        symbols: Sequence[Any] | None = None,
        null_symbol: Any = 0,
        max_clues: int | None = None,
        grid: Optional[GRID_TYPE] = None,
        puzzle: Optional[GRID_TYPE] = None,
    ):
        """Class that can be used for generating Sudoku grid and puzzle.

        Parameters
        ----------
        - number_of_symbols:
            Optional number of symbols that should exist
            in resultant sudoku grid. By default, this is set
            to 9, which is the number of symbols used in a
            traditional Sudoku puzzle.

        - symbols:
            Optional sequence of symbols that would be used
            in Sudoku grid. By default, this will use integer
            values from 1 to number_of_symbols as symbols.
            If both the number_of_symbols and symbols parameters
            exist, the symbols parameter is given more priority,
            and number_of_symbols is set to length of symbols
            sequence.

        - null_symbol:
            Optional symbol that should be used to denote a empty
            cell in sudoku puzzle. This symbol cannot exist in
            the symbols that will be used to create the sudoku
            puzzle. By default, this will use the integer 0.

        - max_clues:
            Optional limit that can be used to set
            how many clues/givens

        - grid:
            Optional array to provide as sudoku grid.
            If this is not provided, a valid sudoku grid
            will be created.

        - puzzle:
            Optional array to provide as sudoku puzzle.
            Note that a new grid will be set in the grid
            attribute.
        """

        if isinstance(symbols, Sequence) and len(symbols) != 0:
            if len(set(symbols)) != len(symbols):
                raise ValueError("Duplicate Symbols not allowed")

            number_of_symbols = len(symbols)
            self._symbols = symbols
        elif number_of_symbols < 1:
            raise ValueError("Provided grid size should be atleast greater than 0")
        else:
            self._symbols = self.generate_default_symbols(number_of_symbols=number_of_symbols)

        self.number_of_symbols = number_of_symbols

        if null_symbol in self.symbols:
            raise ValueError(
                f"Null symbol {null_symbol} needs to be "
                f"distinct from symbols: {', '.join(self.symbols)}"
            )

        self.null_symbol = null_symbol

        if grid is not None:
            self.grid = grid

        if puzzle is not None:
            self.puzzle = puzzle

        if max_clues is not None:
            self.max_clues = max_clues

    def generate_default_symbols(self, *args, number_of_symbols: int, **kwargs) -> Sequence[Any]:
        """Get sequence of default symbols, which is the length of the number_of_symbols."""

        return tuple(range(1, number_of_symbols + 1))

    def is_valid_table_shape(self, array: GRID_TYPE) -> bool:
        """Check whether provided array is a valid sudoku table shape."""

        try:
            return len(array) == self.number_of_symbols and (
                all(len(subarray) == self.number_of_symbols for subarray in array)
            )
        except TypeError:
            return False

    def is_valid_sudoku(self, array: GRID_TYPE) -> bool:
        """Tests whether provided table is a valid sudoku grid matching provided parameters

        References
        ----------
        - https://www.geeksforgeeks.org/dsa/check-if-given-sudoku-solution-is-valid-or-not/
        - https://csourcecodes.blogspot.com/2016/05/c-program-to-validate-sudoku-checking.html
        """

        if not self.is_valid_table_shape(array):
            raise NotSquareArrayError(
                f"Value needs to be a square array of size {self.number_of_symbols}"
            )

        symbols = self.symbols
        symbol_index_lookup = {symbol: index + 1 for index, symbol in enumerate(symbols)}

        rows = [0] * self.number_of_symbols
        cols = [0] * self.number_of_symbols
        blocks = [0] * self.number_of_symbols
        number_of_symbols_sqrt = math.isqrt(self.number_of_symbols)

        for i, j in itertools.product(range(self.number_of_symbols), range(self.number_of_symbols)):
            cell_symbol = array[i][j]
            if cell_symbol not in symbols:
                return False

            symbol_index = 1 << (symbol_index_lookup[cell_symbol] - 1)

            if rows[i] & symbol_index > 0:
                return False

            rows[i] |= symbol_index

            if cols[j] & symbol_index > 0:
                return False

            cols[j] != symbol_index

            block_index = (
                i // number_of_symbols_sqrt
            ) * number_of_symbols_sqrt + j // number_of_symbols_sqrt
            if blocks[block_index] & symbol_index > 0:
                return False
            blocks[block_index] |= symbol_index

        return True

    def get_empty_table(self) -> GRID_TYPE:
        """Get sudoku table where all values are the null_symbol."""

        return [
            [self.null_symbol for _ in range(self.number_of_symbols)]
            for _ in range(self.number_of_symbols)
        ]

    def _get_number_of_symbols(self):
        return self._number_of_symbols

    def _set_number_of_symbols(self, value):
        if value < 1:
            raise ValueError("Provided grid size should be atleast greater than 0")

        self._number_of_symbols = value

    number_of_symbols = property(_get_number_of_symbols, _set_number_of_symbols)

    @property
    def grid(self) -> GRID_TYPE:
        """Returns a completed sudoku grid."""

        if not hasattr(self, "_grid") or self._grid is None:
            self._grid: GRID_TYPE = self.solver(table=self.get_empty_table())

        return self._grid

    @grid.setter
    def grid(self, value):
        if value is None:
            raise ValueError("Grid value cannot be None")

        if not self.is_valid_sudoku(value):
            raise InvalidSudokuError("Provided value is not a valid sudoku")

        self._grid = value

    @property
    def puzzle(self):
        """Returns a puzzle generated from the grid."""

        if not hasattr(self, "_puzzle") or self._puzzle is None:
            self._puzzle: GRID_TYPE = self.generate_puzzle(table=self.grid)

        return self._puzzle

    @puzzle.setter
    def puzzle(self, value):
        if value is None:
            raise ValueError("Puzzle value cannot be None")

        try:
            self.grid = self.solver(table=value)
        except Exception as exc:
            raise InvalidSudokuError("Invalid Sudoku puzzle provided") from exc

        self._puzzle = value

    @property
    def symbols(self):
        """Returns the symbols used in the sudoku grid."""

        return self._symbols

    @property
    def max_cells_to_delete(self) -> int | None:
        """Returns the maximum number of cells that should be deleted during puzzle generation."""

        if not hasattr(self, "_max_cells_to_delete"):
            max_cells_to_delete = None

            max_clues = self.max_clues
            if max_clues is not None and max_clues >= 0:
                total_number_of_cells = self.number_of_symbols * self.number_of_symbols
                max_cells_to_delete = max(total_number_of_cells - max_clues, 0)

            self._max_cells_to_delete = max_cells_to_delete

        return self._max_cells_to_delete

    @max_cells_to_delete.setter
    def max_cells_to_delete(self, value: int | None):
        if value is not None and value < 0:
            raise ValueError("Max cells to delete cannot be less than 0")

        total_number_of_cells = self.number_of_symbols * self.number_of_symbols
        self._max_cells_to_delete = min(value, total_number_of_cells)

    @property
    def max_clues(self) -> int | None:
        """Returns the maximum number of clues/givens to keep in puzzle."""

        return getattr(self, "_max_clues", None)

    @max_clues.setter
    def max_clues(self, value: int | None):
        if not hasattr(self, "_max_clues"):
            if value is not None and value < 0:
                raise ValueError("Max clues cannot be less than 0")

            self._max_clues = value

        return self._max_clues

    def check_safe_to_place(self, table: GRID_TYPE, row: int, col: int, symbol: Any) -> bool:
        """
        Check whether provided symbol is safe to place in the required cell
        denoted using the row and col parameters in the provided table.
        """

        raise NotImplementedError

    def solver(self, *args, table: GRID_TYPE, **kwargs) -> GRID_TYPE:
        """Returns the solved version of the provided table."""

        raise NotImplementedError

    def generate_puzzle(self, *args, table: GRID_TYPE, **kwargs) -> GRID_TYPE:
        """Returns a valid puzzle generated from provided table."""

        raise NotImplementedError
