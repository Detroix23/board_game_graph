"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/definitions.py

Constant and hard-coded values.
"""
import pathlib
import enum
from typing import Final

import numpy

Player = numpy.uint8

Board = numpy.ndarray[tuple[int], numpy.dtype[Player]]

BoardList = numpy.ndarray[tuple[int, int], numpy.dtype[Player]]

ImageList = numpy.ndarray[tuple[int], numpy.dtype[numpy.uint32]]

GraphBoard = dict[Board, BoardList]

Graph = dict[int, ImageList]


PATH_GRAPHS: Final[pathlib.Path] = pathlib.Path("./data/graphs")
PATH_GRAPHVIZ: Final[pathlib.Path] = pathlib.Path("./data/graphviz")
PATH_PYVIS: Final[pathlib.Path] = pathlib.Path("./data/pyvis")

PATH_WINS: Final[pathlib.Path] = pathlib.Path("./data/wins")

DIRECTIONS: Final[list[tuple[int, int]]] = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
]

PLAYER_SYMBOLS: Final[list[str]] = [" ", "X", "O", "Δ", "┼", "Z"]

PLAYER_COLORS: Final[list[str]] = []

DEFAULT_FILE_FORMAT: Final[str] = "svg"

DEFAULT_GRAPHVIZ_ENGINE: Final[str] = "dot"

class FileFormat(enum.Enum):
    """
    # `FileFormat` for exporting.
    """
    DEFAULT = 0
    SVG = 1
    PNG = 2
    
    def to_str(self) -> str:
        """
        Convert this enumeration to its `str` representation.
        """
        if self != FileFormat.DEFAULT:
            return self.name.lower()
        else:
            return DEFAULT_FILE_FORMAT
        
    def __str__(self) -> str:
        """
        Returns the readable name of an option.
        """
        return self.name

class LayoutEngine(enum.Enum):
    """
    # `LayoutEngine`s for `graphviz`.

    From:
    > https://graphviz.org/docs/layouts/
    """
    DEFAULT = 0
    DOT = 1
    """ **Graphviz**. Hierarchical or layered drawings of directed graphs. """
    NEATO = 2
    """ **Graphviz**. Spring model layouts. """
    FDP = 3
    """ **Graphviz**. Force-Directed Placement. """
    SFDP = 4
    """ **Graphviz**. Scalable Force-Directed Placement. """
    CIRCO = 5
    """ **Graphviz**. Circular layout. """
    TWOPI = 6
    """ **Graphviz**. Radial layout. """
    OSAGE = 9
    """ **Graphviz**. Draws clustered graphs. """
    PATCHWORK = 10
    """ **Graphviz**. Draws map of clustered graph using a squarified tree-map layout. """
    PYVIS = 11
    """ **Pyvis**. HTML-JSON interactive render. """

    def to_str(self) -> str:
        """
        Convert this enumeration to its `str` representation.
        """
        if self != LayoutEngine.DEFAULT:
            return self.name.lower()
        else:
            return DEFAULT_GRAPHVIZ_ENGINE

    def __str__(self) -> str:
        """
        Returns the readable name of an option.
        """
        return self.name