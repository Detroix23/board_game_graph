"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/plays.py
"""
from typing import Optional

import numpy

from tic_tac_toe_detroix23.definitions import Board, BoardsNext, Graph
from tic_tac_toe_detroix23 import configurations

def next_player(player: int, player_count: int) -> int:
    """
    Cycle from the current `player` to next player.
    """
    return player % player_count + 1

def generate_plays_graph(
    board: Board, 
    size: tuple[int, int],
    player: int,
    player_count: int,
    depth: int = -1,
    graph: Optional[Graph] = None,
) -> Graph:
    """
    Recursively discovers and maps the `Graph`:
    - starting from `board`;
    - for many `depth` steps.

    **Arguments**:
    - `board`: starting configuration;
    - `size`: 2D size of the `board`;
    - `player`: starting player ID;
    - `player_count`: used to cycle turns;
    - `depth`: limit the recursion. `-1` to remove the limit;
    - `graph`: built graph, passed in the recursion.
    """
    if depth == 0:
        return (graph
            if graph is not None
            else {}
        )
    
    graph_update: Graph = (graph
        if graph is not None
        else {}
    )

    next_boards: Optional[BoardsNext] = next_board(board, size, player)
    
    if next_boards is not None:
        graph_update[configurations.image(board, player_count + 1)] = numpy.array([
            numpy.uint32(configurations.image(child, player_count + 1))
            for child in next_boards
        ])

        for child in next_boards:
            if configurations.image(child, player_count + 1) not in graph_update.keys():
                graph_update |= generate_plays_graph(
                    child,
                    size,
                    next_player(player, player_count),
                    player_count,
                    depth - 1,
                    graph,
                )

    return graph_update

def next_board(
    board: Board,
    size: tuple[int, int],
    player: int,
) -> Optional[BoardsNext]:
    """
    Returns all possible `Configuration` after the turn of `player`. 
    """
    if configurations.is_full(board):
        return None

    return numpy.vstack(tuple(
        configurations.update_index(board.copy(), index, player)
        for index in range(len(board))
        if board[index] == 0
    ))
