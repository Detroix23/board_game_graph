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

Graph = dict[int, numpy.ndarray[tuple[int], numpy.dtype[numpy.uint32]]]


PATH_GRAPH: Final[pathlib.Path] = pathlib.Path("./data/graphs")

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
        
class LayoutEngine(enum.Enum):
    """
    # `LayoutEngine`s for `graphviz`.

    From:
    > https://graphviz.org/docs/layouts/
    """
    DEFAULT = 0
    DOT = 1
    """ Hierarchical or layered drawings of directed graphs. """
    NEATO = 2
    """ Spring model layouts. """
    FDP = 3
    """ Force-Directed Placement. """
    SFDP = 4
    """ Scalable Force-Directed Placement. """
    CIRCO = 5
    """ Circular layout. """
    TWOPI = 6
    """ Radial layout. """
    OSAGE = 9
    """ Draws clustered graphs. """
    PATCHWORK = 10
    """ Draws map of clustered graph using a squarified tree-map layout. """

    def to_str(self) -> str:
        """
        Convert this enumeration to its `str` representation.
        """
        if self != LayoutEngine.DEFAULT:
            return self.name.lower()
        else:
            return DEFAULT_GRAPHVIZ_ENGINE
