"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/cli.py
"""
from typing import Final, TypeVar, Type

from tic_tac_toe_detroix23.definitions import Board, Graph, FileFormat, LayoutEngine
from tic_tac_toe_detroix23 import (
    configurations, plays, conditions, graphs, ui, exports, graphing
)

HELP: Final[str] = """
## Help.

CLI arguments:
- "h", "help":
    Prints this help.

- "t", "assertions":
    tests.configurations1()
    tests.next_configuration1()

- "tbg1":
    tests.generate_board_graph1()

- "tbg2":
    tests.generate_board_graph2()

- "twc1":
    tests.win_conditions1()

- "r", "reverse":
    cli.reverse_image()

- "g", "graph":
    cli.draw_graph()

"""

_T_INPUT = TypeVar("_T_INPUT")

def get_input(
    input_type: Type[_T_INPUT],
    message: str,
    default: _T_INPUT,
) -> _T_INPUT:
    """
    Get user input and returns converted to `_T_INPUT`.
    """
    user_input: str = input(f"{message} [{input_type.__name__}]({default}): ")
    output: _T_INPUT

    if not user_input:
        output = default
    
    else:
        try:
            output = input_type(user_input)  # pyright: ignore[reportCallIssue]
        
        except TypeError:
            output = default
    
    print(f"=> `{output}`")
    return output

def reverse_image() -> None:
    """
    Input loop to convert input `code` to a board.
    """
    print("## Reverse image.\n")
    player_count: int = 2
    size: tuple[int, int] = (3, 3)
    print(f"""With:
- player_count={player_count};
- size={size}.
""")
    try: 
        while True:
            code: str = input("\ncode: ")
            print(ui.format_board(configurations.reverse_image(
                int(code),
                player_count + 1,
                size[0] * size[1],
            ), size))

    except KeyboardInterrupt as interrupt:
        print(f"\nInterrupted by CTRL+C. Details: \n```\n{interrupt}\n```\n")

    return

def draw_graph() -> None:
    """
    Input loop to create a graph from an interactive CLI.
    """
    print("## Custom graph.\n")

    try:    
        player_count: int = get_input(int, "Player count", 2)
        player_start: int = get_input(int, "Starting player", 2)
        size: tuple[int, int] = (
            get_input(int, "Size X of the board", 3),
            get_input(int, "Size Y of the board", 3),
        )
        win_length: int = get_input(int, "Aligned length to win", 3)
        file_format: FileFormat = FileFormat.SVG
        layout_engine: LayoutEngine = LayoutEngine.NEATO

        print(f"""Global parameters:
  - player_count={player_count};
  - player_start={player_start};
  - size={size};
  - win_length={win_length};
  - file_format={file_format};
  - layout_engine={layout_engine};
    """)

        while True:
            print("\n### Graph settings [constraint](default).")
            node_start: int = get_input(int, "Node code", 0)
            depth: int = get_input(int, "Depth", -1)

            print("\n### Generation.")

            board_start: Board = configurations.reverse_image(
                node_start,
                player_count + 1,
                size[0] * size[1],
            )

            win_conditions = conditions.WinConditions(
                size,
                player_count,
                win_length,
            )
            win_conditions.generate()

            graph: Graph = plays.generate_graph(
                board_start,
                size,
                player_start,
                player_count,
                win_conditions,
                depth,
            )

            # Data analysis.
            print("\n### Data analysis:")

            print(f"Graph node count: \n  q={len(graph)}")

            graph_index = graphs.indexing(
                graph,
                node_start,
                player_start,
                player_count,
                win_conditions,
                depth_start=0,
            )

            ## Collecting end states:
            end_states: dict[int, int] = {
                -1: 0,
                0: 0,
                1: 0,
                2: 0,
            }
            for node_state in graph_index:
                end_states[node_state.win_state] += 1

            print("End states: ")
            for win_state, count in end_states.items():
                print(f"  {win_state}: {count};")

            # Exporting and graphing.
            print("\n### Outputs.")
            name: str = f"manual{node_start}_{size[0]}x{size[1]}_d{depth}"
            
            
            exports.play_graph(
                f"ttt_{name}", 
                graph, 
                size, 
                1, 
                player_count,
                2
            )

            if depth != -1 and depth <= 3:
                graph_drawer = graphing.GraphDrawer(
                    name,  
                    graph,
                    graph_index,
                    configurations.image(board_start, player_count + 1),
                    player_start,
                    player_count,
                    win_conditions,
                    file_format,
                    layout_engine,
                )
                graph_drawer.draw()

    except KeyboardInterrupt as interrupt:
        print(f"\nInterrupted by CTRL+C. Details: \n```\n{interrupt}\n```\n")

    return
