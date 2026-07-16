"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/conditions.py
"""
import time

from tic_tac_toe_detroix23.definitions import Board, DIRECTIONS
from tic_tac_toe_detroix23 import configurations


class WinConditions:
    """
    # Pre-generate and compare `WinConditions`.
    """
    size: tuple[int, int]
    player_count: int
    win_length: int
    _win_images: dict[int, int]
    """ Stores all the win configuration as `int` images. """

    def __init__(
        self,
        size: tuple[int, int],
        player_count: int,
        win_length: int,
    ) -> None:
        """
        Instantiate the `WinConditions` generator.
        Does generate the conditions.
        """
        self.size = size
        self.player_count = player_count
        self.win_length = win_length
        
        self.generate()

        return

    def get_win_images(self) -> dict[int, int]:
        """
        Returns the read-only attributes `_win_image`.
        """
        return self._win_images
    
    def tile_wining_schemas(
        self,
        x: int,
        y: int,
        size: tuple[int, int],
        player_count: int,
    ) -> list[tuple[Board, int]]:
        """
        Returns a `list` of `tuple` of:
        1. configuration images:
            - made of only wining position;
            - for all players [`1`; `player_count`];
            - other tiles are blank (`0`). 
        2. winning player.
        """
        schema_player: int = 1
        schemas: list[tuple[Board, int]] = []

        for direction in DIRECTIONS:
            board: Board = configurations.empty(size)
            valid: bool = True
            steps: int = 0
            u: int = x
            v: int = y
            while valid and steps < 3:
                configurations.update(
                    board,
                    size,
                    u,
                    v,
                    schema_player,
                )

                steps += 1
                u += direction[0]
                v += direction[1] 
                if steps < 3:           
                    valid = 0 <= u < size[0] and 0 <= v < size[1]

            if valid:
                schemas.append((board, 1))
                for player_id in range(2, player_count + 1):
                    schemas.append((configurations.replace(
                        board.copy(), 
                        player_id - 1, 
                        player_id,
                    ), player_id))

        return schemas

    def fill_combinations(
        self,
        board: Board,
        index: int = 0,
        fill: int = 0,
    ) -> list[int]:
        """
        Recursively fill the tiles `fill` of the `board` 
        with all possible combinations.

        Returns a `list` of `int` images. 
        """
        if index >= len(board):
            return [configurations.image(board, self.player_count + 1)]

        elif board[index] != fill:
            return self.fill_combinations(
                board,
                index + 1,
                fill,
            )
        
        else:
            return [
                combination
                for player_id in range(self.player_count + 1)
                for combination in self.fill_combinations(
                    configurations.update_index(
                        board.copy(), 
                        index, 
                        player_id
                    ),
                    index + 1,
                    fill,
                )
            ]

    def generate(self) -> dict[int, int]:
        """
        Precompute all wining board in a `BoardList`,
        where winning is lining `win_length` plays.
        """
        print("(?) conditions.WinConditions.generate() Start...")
        time_start: float = time.perf_counter()

        # Generate schemas:
        # - all wining positions for all player [1; `player_count`];
        # - all non wining tiles are `0`.
        schemas: list[tuple[Board, int]] = []
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                schemas += self.tile_wining_schemas(
                    x,
                    y,
                    self.size,
                    self.player_count,
                )

        # Fill the win schemas' `0`s with all possible combinations.
        # Maximum image count:
        # _image_count: int = len(schemas) * (player_count + 1) ** (size[0] * size[1] - win_length)
        images: dict[int, int] = dict()

        for schema, player in schemas:
            images |= {
                combination: player
                for combination in self.fill_combinations(
                    schema,
                    index=0,
                    fill=0,
                )
            }
        
        time_elapsed: float = time.perf_counter() - time_start
        print(f"(?) conditions.WinConditions.generate() End in {time_elapsed:.2f}s.")
        self._win_images = images
        return self._win_images

    def is_win(
        self,
        image: int
    ) -> bool:
        """
        Returns `True` if `board` is in a winning condition.
        """
        return image in self._win_images.keys()
    
    def get_winner(self, image: int) -> int:
        """
        Returns an `int` code of the winner of the given `image`:
        - `= -1` game is not interrupted;
        - `> 0` is the ID of the player that wins.
        """
        return self._win_images.get(image, -1)
    
    