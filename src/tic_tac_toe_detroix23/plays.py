"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/plays.py
"""
import time
from typing import Optional

import numpy

from tic_tac_toe_detroix23.definitions import Board, BoardList, Graph
from tic_tac_toe_detroix23 import configurations, conditions

def next_player(player: int, player_count: int) -> int:
    """
    Cycle from the current `player` to next player.
    """
    return player % player_count + 1

def next_board(
    board: Board,
    size: tuple[int, int],
    player: int,
) -> Optional[BoardList]:
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

def generate_graph(
    board: Board, 
    size: tuple[int, int],
    player: int,
    player_count: int,
    win_condition: conditions.WinConditions,
    depth: int = -1,
) -> Graph:
    """
    Recursively discovers and maps the `Graph`:
    - starting from `board`;
    - for many `depth` steps.

    **Arguments**:
    - `board`: starting configuration;
    - `size`: 2D size of the `board`;
    - `player`: starting player ID that just played `board`;
    - `player_count`: used to cycle turns;
    - `depth`: limit the recursion. `-1` to remove the limit;
    - `graph`: built graph, passed in the recursion.
    """
    print(f"(?) plays.generate_graph(depth={depth}) Start...")
    time_start: float = time.perf_counter()

    def generate_graph_body(
        board: Board, 
        player: int,
        depth: int,
        graph: Graph,
    ) -> Graph:
        if depth == 0:
            return graph

        image_board: int = configurations.image(board, player_count + 1)

        if win_condition.is_win(image_board):
            graph[image_board] = numpy.empty(
                (0,), 
                dtype=numpy.uint32
            )
            return graph
        
        next_boards: Optional[BoardList] = next_board(board, size, player)
        
        if next_boards is not None:
            graph[image_board] = numpy.array([
                numpy.uint32(configurations.image(child, player_count + 1))
                for child in next_boards
            ])

            for child in next_boards:
                image: int = configurations.image(child, player_count + 1)
                if image not in graph.keys():
                    graph |= generate_graph_body(
                        child,
                        next_player(player, player_count),
                        depth - 1,
                        graph,
                    )

        return graph

    time_elapsed: float = time.perf_counter() - time_start
    print(f"(?) plays.generate_graph(depth={depth}) End in {time_elapsed:.2f}s.")
    return generate_graph_body(
        board,
        player,
        depth,
        {}
    )
