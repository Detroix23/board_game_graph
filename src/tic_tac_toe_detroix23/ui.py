"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/ui.py
"""
from tic_tac_toe_detroix23.definitions import Graph, Board, PLAYER_SYMBOLS

def format_graph(graph: Graph) -> str:
    """
    Returns a formatted string of `graph`.
    """
    return "\n".join([
        f"- {node}: {neighbors};"
        for node, neighbors in graph.items()
    ])

def format_board(board: Board, size: tuple[int, int]) -> str:
    """
    Returns a formatted string of `board` according to `size`
    """
    return f"\n{(size[0]-1)*'─┼'}─\n".join([
        "|".join([
            PLAYER_SYMBOLS[int(board[y * size[0] + x])]
            for x in range(size[0])
        ])
        for y in range(size[1])
    ]) + "\n"
