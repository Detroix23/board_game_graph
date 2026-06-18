"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/configuration.py
"""
import numpy

from utilities.debug import assert_eq
from tic_tac_toe_detroix23.definitions import Board

class Configuration:
    """
    # A tic-tac-toe `Configuration`.
    Define a state of the board in a 1 dimension `list` `data`.

    **Players**:
    - `0` is empty;
    - `[1; player_count]` valid players.

    **Attributes**:
    - `size`: `tuple[int, int]`
    - `player_count`: `int`
    - `data`: `list[int]`

    **Data storage** (`data`):

    Represents the board in a 1D list. 
    
    _Example_:
    
    - From:

        |0;0|1;0|2;0|       |0 |1 |2 |
        |0;1|1;1|2;1|       |3 |4 |5 |
        |0;2|1;2|2;2|       |6 |7 |8 |

    - To:

        [0, 1, 2, 3, 4, 5, 6, 7, 8] 

    """
    size: tuple[int, int]
    player_count: int
    data: Board

    def __init__(
        self,
        size: tuple[int, int],
        player_count: int,
        data: Board,
    ) -> None:
        """
        Create a `Configuration`.
        """
        self.size = size
        self.player_count = player_count
        self.data = data

    def __repr__(self) -> str:
        """
        Returns an evaluation-valid `Configuration` representation.
        """
        return f"Configuration(size={self.size}, player_count={self.player_count}, \
data={self.data})"

    @staticmethod
    def new_empty(
        size: tuple[int, int], 
        player_count: int,
    ) -> 'Configuration':
        """
        Create a 0-filled (empty) configuration.
        """
        return Configuration(
            size,
            player_count,
            empty(size)
        )

    def clone(self) -> 'Configuration':
        """
        Create an _unlinked_-copy of `self.`
        """
        return Configuration(
            self.size,
            self.player_count,
            self.data.copy(),
        )

    def to_int(self) -> int:
        """
        Returns the `int` identifier of this configuration.
        """
        return image(self.data, self.player_count + 1)
            
    def get(self, x: int, y: int) -> int:
        """
        Get the player ID in the configuration 
        at coordinates (`x`; `y`).
        """
        return get(self.data, self.size, x, y)

    def update(self, x: int, y: int, player: int) -> None:
        """
        Update the player ID in the configuration 
        at coordinates (`x`; `y`)
        with new `player` id.
        """
        update(self.data, self.size, x, y, player)
        return
    
    def is_full(self) -> bool:
        """
        Returns `True` if all tiles are different of `0`.
        - `0` is an empty tile.
        """
        return 0 not in self.data


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
