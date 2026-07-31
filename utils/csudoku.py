"""Contains Sudoku classes that make use of the numpy library for better optimization."""

import numpy as np

from .custom_types import GRID_TYPE
from .sudoku import SquareSudoku


class CSudoku(SquareSudoku):
    """Class for generating square sudoku puzzles.

    This class utilises the numpy library for its
    operations as it provides better memory management
    and can be slightly more optimized.

    Note that provided null symbol data type will be
    updated to match that of the resultant grid and puzzle.
    It is thus advised to use the null_symbol attribute
    for any operations where the null symbol needs to be used.
    """

    def get_empty_table(self):
        """
        Returns an empty square array with provided
        number_of_symbols as length.

        Note that provided null symbol data type
        will be updated to match the data type
        of the resultant empty square array
        to avoid unexpected errors.
        """

        empty_table = np.full(
            (self.number_of_symbols, self.number_of_symbols),
            self.null_symbol,
            dtype=np.array(self.symbols).dtype,
        )

        self.null_symbol = np.array(self.null_symbol).astype(empty_table.dtype).item()

        return empty_table

    def create_table_copy(self, table: GRID_TYPE) -> GRID_TYPE:
        """Return a copy of provided table."""

        return np.array(table)

    def generate_default_symbols(self, *args, number_of_symbols: int, **kwargs):
        """Get sequence of default symbols, which is the length of the number_of_symbols."""

        return np.arange(1, number_of_symbols + 1)

    @property
    def symbols(self):
        """Symbols used in grid provided in a random order"""

        if isinstance(self._symbols, str):
            self._symbols = tuple(self._symbols)

        return np.random.permutation(self._symbols)

    def get_grid_indices(self, random_: bool = True):
        """Returns list of indices of a grid in optional randomized order.

        References
        ----------
        - https://stackoverflow.com/questions/11144513#answer-11146645
        """

        arr = np.empty((self.number_of_symbols, self.number_of_symbols, 2), dtype=np.int64)
        for index, array in enumerate(
            np.ix_(np.arange(self.number_of_symbols), np.arange(self.number_of_symbols))
        ):
            arr[..., index] = array

        result_arr = arr.reshape(-1, 2)
        if random_ is True:
            np.random.shuffle(result_arr)

        return result_arr
