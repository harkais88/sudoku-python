from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    try:
        import numpy as np  # noqa: F401
        import numpy.typing as npt  # noqa: F401
    except ImportError:
        pass

GRID_TYPE: TypeAlias = (
    "list[list[int | float]] | npt.NDArray[np.integer] | npt.NDArray[np.floating]"
)
