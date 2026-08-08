"""Common utils needed by the Sudoku Games"""

import copy
import itertools
import logging
import math
import random
from typing import Sequence

from .abstract import SudokuAbstract
from .custom_types import GRID_TYPE
from .exceptions import NotSquareArrayError

logger = logging.getLogger(__name__)


class SudokuBacktracking(SudokuAbstract):
    """Class for generating sudoku grids using backtracking."""

    @property
    def number_of_symbols_square_root(self):
        """Get the square root of the provided number of symbols"""

        if hasattr(self, "_number_of_symbols_square_root"):
            return self._number_of_symbols_square_root

        self._number_of_symbols_square_root: int = math.isqrt(self.number_of_symbols)
        return self._number_of_symbols_square_root

    def create_table_copy(self, table: GRID_TYPE) -> GRID_TYPE:
        """Return a copy of provided table.

        According to the official Python documentation,
        Assignment statements in Python do not copy objects,
        they create bindings between a target and an object.
        For collections that are mutable or contain mutable
        items, a copy is sometimes needed so one can change
        one copy without changing the other.

        Therefore, this is required for the cases where
        the provided table needs to be kept intact while
        also getting a copy of it.

        Reference
        ---------
        - https://docs.python.org/3/library/copy.html
        """

        return copy.deepcopy(table)

    @property
    def symbols(self):
        """Symbols used in grid provided in a random order"""

        return random.sample(self._symbols, k=self.number_of_symbols)

    def solver(self, *args, table: GRID_TYPE, row=0, col=0, **kwargs):
        """Solves a sudoku puzzle using backtracking"""

        _table = table
        if row == 0 and col == 0:
            _table = self.create_table_copy(table=table)

        if row == self.number_of_symbols - 1 and col == self.number_of_symbols:
            return _table

        if col == self.number_of_symbols:
            row += 1
            col = 0

        if _table[row][col] != self.null_symbol:
            return self.solver(*args, table=_table, row=row, col=col + 1, **kwargs)

        for symbol in self.symbols:
            if not self.check_safe_to_place(table=_table, row=row, col=col, symbol=symbol):
                continue

            _table[row][col] = symbol
            solved_table = self.solver(*args, table=_table, row=row, col=col + 1, **kwargs)
            if solved_table is not None:
                return solved_table

            _table[row][col] = self.null_symbol

        return None

    def check_safe_to_place(self, table, row, col, symbol) -> bool:
        """Checks if symbol is safe to place in a cell specified by row and col"""

        if self.check_symbol_in_row(table=table, row=row, symbol=symbol) is True:
            return False

        if self.check_symbol_in_col(table=table, col=col, symbol=symbol) is True:
            return False

        return self.check_symbol_in_block(
            table=table,
            row=row - row % self.number_of_symbols_square_root,
            col=col - col % self.number_of_symbols_square_root,
            symbol=symbol,
        )

    def check_symbol_in_row(self, table, row, symbol) -> bool:
        return symbol in table[row]

    def check_symbol_in_col(self, table, col, symbol) -> bool:
        for i in range(self.number_of_symbols):
            if table[i][col] == symbol:
                return True
        return False

    def check_symbol_in_block(self, table, row, col, symbol) -> bool:
        """
        Check if symbol is safe to place in a block identified
        by its upper leftmost row and col
        """

        for i in range(self.number_of_symbols_square_root):
            if row + i >= self.number_of_symbols:
                break

            for j in range(self.number_of_symbols_square_root):
                if col + j >= self.number_of_symbols:
                    break

                if table[row + i][col + j] == symbol:
                    return False

        return True

    def get_grid_indices(self, random_: bool = True) -> Sequence[tuple[int, int]]:
        """Returns list of indices of a grid in optional randomized order."""

        grid_indices = list(
            itertools.product(range(0, self.number_of_symbols), range(0, self.number_of_symbols))
        )

        if random_ is True:
            random.shuffle(grid_indices)

        return grid_indices

    def generate_puzzle(self, *args, table: GRID_TYPE, **kwargs):
        """Generates a unique_puzzle from a completed grid

        References
        ----------
        - https://stackoverflow.com/questions/6924216#answer-7280517
        """

        _table = self.create_table_copy(table)
        indices = self.get_grid_indices(random_=True)

        total_number_of_cells = self.number_of_symbols * self.number_of_symbols
        max_cells_to_delete = self.max_cells_to_delete or total_number_of_cells

        for row, col in indices:
            logger.debug(f"Trying for row {row} and col {col}")
            if _table[row][col] == self.null_symbol:
                logger.debug("Null symbol encountered, skipping this...")
                max_cells_to_delete -= 1
                continue

            if max_cells_to_delete == 0:
                break

            cell_symbol = _table[row][col]
            _table[row][col] = self.null_symbol
            for symbol in self.symbols:
                if symbol == cell_symbol or (
                    not self.check_safe_to_place(table=_table, row=row, col=col, symbol=symbol)
                ):
                    continue

                logger.debug(
                    f"Symbol {symbol} possible to place, "
                    "checking whether duplicate solution exists..."
                )
                _table[row][col] = symbol
                solved = self.solver(table=self.create_table_copy(_table))
                if solved is not None:
                    logger.debug("Duplicate symbol exists, not deleting current cell...")
                    _table[row][col] = cell_symbol
                    break

                _table[row][col] = self.null_symbol

            if _table[row][col] == self.null_symbol:
                max_cells_to_delete -= 1

        return _table

    def get_printable_table(self, table):
        """Prints the table in square sudoku format"""

        if not self.is_valid_table_shape(array=table):
            raise NotSquareArrayError("Provided table is not valid shape")

        result = "\n"
        border_length = 0
        for i in range(self.number_of_symbols):
            for j in range(self.number_of_symbols):
                if table[i][j] != self.null_symbol:
                    value_result = f" {table[i][j]} "
                else:
                    value_result = "   "

                result += value_result
                border_length += len(value_result)

                if ((j + 1) % self.number_of_symbols_square_root == 0) and (
                    j != self.number_of_symbols - 1
                ):
                    result += " | "
                    border_length += 3

            result += "\n"
            if ((i + 1) % self.number_of_symbols_square_root == 0) and (
                i != self.number_of_symbols - 1
            ):
                result += "-" * border_length + "\n"

            border_length = 0

        result += "\n"
        return result


class SquareSudoku(SudokuBacktracking):
    """Class for generating square sudoku puzzles"""

    @SudokuBacktracking.number_of_symbols.setter
    def number_of_symbols(self, value):
        if SudokuBacktracking.number_of_symbols.fset is None:
            raise NotImplementedError("number_of_symbols property setter not found")

        sqrt = math.isqrt(value)
        if sqrt * sqrt != value:
            raise ValueError("Number of symbols needs to be a perfect square.")

        SudokuBacktracking.number_of_symbols.fset(self, value)
