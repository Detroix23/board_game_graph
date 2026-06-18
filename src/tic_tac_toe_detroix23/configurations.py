"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/configuration.py
"""
import numpy
from numpy.typing import NDArray

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
    data: NDArray[numpy.int8]

    def __init__(
        self,
        size: tuple[int, int],
        player_count: int,
        data: NDArray[numpy.int8],
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
            numpy.zeros((size[0] * size[1],), dtype=numpy.int8)
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
        return base10(self.data, self.player_count + 1)
            
    def get(self, x: int, y: int) -> int:
        """
        Get the player ID in the configuration 
        at coordinates (`x`; `y`).
        """
        return self.data[self.size[1] * y + x]

    def update(self, x: int, y: int, player: int) -> None:
        """
        Update the player ID in the configuration 
        at coordinates (`x`; `y`)
        with new `player` id.
        """
        self.data[self.size[1] * y + x] = player
        return
    
    def is_full(self) -> bool:
        """
        Returns `True` if all tiles are different of `0`.
        - `0` is an empty tile.
        """
        return 0 not in self.data


def base10(array: NDArray, base: int) -> int:
    """
    Convert any `array` of digits of base `base` to base 10.
    """
    return sum(
        int(array[-(index + 1)]) * base ** index 
        for index in range(len(array))
    )
