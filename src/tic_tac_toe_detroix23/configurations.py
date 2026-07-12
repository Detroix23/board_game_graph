"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/configuration.py
"""
import numpy

from utilities.debug import assert_eq
from tic_tac_toe_detroix23.definitions import Board

def empty(size: tuple[int, int]) -> Board:
    """
    Create a 0-filled (empty) configuration.
    """
    return numpy.zeros(
        (size[0] * size[1],), 
        dtype=numpy.uint8
    )

def image(array: Board, base: int) -> int:
    """
    Convert an `array` of digits of base `base` to base 10.
    """
    return sum(
        int(array[-(index + 1)]) * base ** index 
        for index in range(len(array))
    )

def reverse_image(n: int, base: int, size: int) -> Board:
    """
    Find the `Board` which matches `image`. 
    ```python
    assert board == reverse_image(image(board, base), base, size=len(board))
    ```
    """
    board: Board = numpy.zeros((size,), dtype=numpy.uint8)
    index: int = size - 1

    remains: int = n
    while index >= 0:
        for digit in range(base - 1, 0, -1):
            value: int = digit * base ** index
            if value <= remains:
                remains -= value
                board[-(index + 1)] = numpy.uint8(digit)
        index -= 1

    assert_eq(image(board, base), n)

    return board


def get(
    board: Board, 
    size: tuple[int, int],
    x: int, 
    y: int,
) -> int:
    """
    Get the player ID in the configuration `board` 
    at coordinates (`x`; `y`).
    """
    return board[size[0] * y + x]

def update(
    board: Board,
    size: tuple[int, int],
    x: int, 
    y: int, 
    player: int,
) -> Board:
    """
    Update the player ID in the configuration 
    at coordinates (`x`; `y`)
    with new `player` id.
    """
    board[size[0] * y + x] = player
    return board

def update_index(
    board: Board,
    index: int,
    player: int,
) -> Board:
    """
    Update the tile `index` of `board` with `player`.
    """
    board[index] = player
    return board

def is_full(board: Board) -> bool:
    """
    Returns `True` if all tiles are different of `0`.
    - `0` is an empty tile.
    """
    return 0 not in board

def replace(
    board: Board,
    origin: int,
    destination: int,
) -> Board:
    """
    Returns an updated `board` where 
    all tiles of player ID `origin`
    are replaced by `destination` player ID.
    """
    for index in range(len(board)):
        if board[index] == origin:
            board[index] = destination
    
    return board
