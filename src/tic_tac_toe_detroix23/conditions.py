"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/conditions.py
"""
from tic_tac_toe_detroix23.definitions import Board, DIRECTIONS
from tic_tac_toe_detroix23 import configurations


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

def tile_wining_schemas(
    x: int,
    y: int,
    size: tuple[int, int],
    player_count: int,
) -> list[Board]:
    """
    Returns a `list` of configuration images:
    - made of only wining position;
    - for all players [1; `player_count`];
    - other tiles are blank (`0`). 
    """
    schema_player: int = 1
    schemas: list[Board] = []

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
            schemas.append(board)
            for player_id in range(2, player_count + 1):
                schemas.append(replace(
                    board.copy(), 
                    player_id - 1, 
                    player_id,
                ))

    return schemas

def fill_combinations(
    board: Board,
    player_count: int,
    index: int = 0,
    fill: int = 0,
) -> set[int]:
    """
    Recursively fill the tiles `fill` of the `board` 
    with all possible combinations.

    Returns a `list` of `int` images. 
    """
    if index >= len(board):
        return {configurations.image(board, player_count + 1)}

    elif board[index] != fill:
        return fill_combinations(
            board,
            player_count,
            index + 1,
            fill,
        )
    
    else:
        combinations: set[int] = set() 
        for player_id in range(player_count + 1):
            combinations |= fill_combinations(
                configurations.update_index(
                    board.copy(), 
                    index, 
                    player_id
                ),
                player_count,
                index + 1,
                fill,
            )

        return combinations

def generate_wining_boards(
    size: tuple[int, int], 
    player_count: int,
    win_length: int
) -> set[int]:
    """
    Precompute all wining board in a `BoardList`,
    where winning is lining `win_length`.
    """
    # Generate schemas:
    # - all wining positions for all player [1; `player_count`];
    # - all non wining tiles are `0`.
    schemas: list[Board] = []
    
    for y in range(size[1]):
        for x in range(size[0]):
            schemas += tile_wining_schemas(
                x,
                y,
                size,
                player_count,
            )

    print(f"q(schemas)={len(schemas)}")

    # Fill the win schemas' `0`s with all possible combinations.
    # Maximum image count:
    # _image_count: int = len(schemas) * (player_count + 1) ** (size[0] * size[1] - win_length)
    images: set[int] = set()

    for schema in schemas:
        images |= fill_combinations(
            schema,
            player_count,
            index=0,
            fill=0,
        )
        
    return images

def is_win(board: Board) -> bool:
    """
    Returns `True` if `board` is in a winning condition.
    """
    ...
