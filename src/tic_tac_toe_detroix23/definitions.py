"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/definitions.py

Constant and hard-coded values.
"""
import pathlib
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
