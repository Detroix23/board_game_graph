"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/ui.py
"""
from tic_tac_toe_detroix23.definitions import Graph, Board, PLAYER_SYMBOLS

def format_graph(graph: Graph) -> str:
    """
    Returns a formatted string of `graph`.

    _Example_:

        - 0: 6561 2187 729 243 81 27 9 3 1;
        - 6561: 10935 8019 7047 6723 6615 6579 6567 6563;
        - 10935: 11664 11178 11016 10962 10944 10938 10936;
        - 8019: 10206 8262 8100 8046 8028 8022 8020;
        - 7047: 9234 7776 7128 7074 7056 7050 7048;
        - 6723: 8910 7452 6966 6750 6732 6726 6724;
        - 6615: 8802 7344 6858 6696 6624 6618 6616;
        ...
    """
    return "\n".join([
        f"- {node}: {" ".join(str(neighbor) for neighbor in neighbors)};"
        for node, neighbors in graph.items()
    ])

def format_board(
    board: Board, 
    size: tuple[int, int],
    vertical: str = "│",
    horizontal: str = "─",
    intersection: str = "┼",
    lines: str = "\n",
    player_symbols: list[str] = PLAYER_SYMBOLS 
) -> str:
    """
    Returns a formatted string of `board` according to `size`
    
    _Example_:

         │ │    
        ─┼─┼─    
         │O│X    
        ─┼─┼─
        O│O│     
    """
    return f"\n{(size[0]-1)*(horizontal + intersection)}{horizontal}{lines}".join([
        vertical.join([
            player_symbols[int(board[y * size[0] + x])]
            for x in range(size[0])
        ])
        for y in range(size[1])
    ]) + "\n"
