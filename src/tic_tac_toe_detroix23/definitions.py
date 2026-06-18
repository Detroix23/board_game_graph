"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/definitions.py

Constant and hard-coded values.
"""
import pathlib
from typing import Final

import numpy

Player = numpy.uint8

Board = numpy.typing.NDArray[Player]

BoardsNext = numpy.ndarray[tuple[int, int], numpy.dtype[Player]]

GraphBoard = dict[Board, BoardsNext]

Graph = dict[int, numpy.ndarray[tuple[int], numpy.dtype[numpy.uint32]]]


PATH_GRAPH: Final[pathlib.Path] = pathlib.Path("./data")