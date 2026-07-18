"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/cli.py
"""
import time
import enum
from typing import Final, TypeVar, Type

from utilities.definitions import FileFormat
from utilities import graphing, graphviz_wrapper, pyvis_wrapper
from tic_tac_toe_detroix23.definitions import Board, Graph, LayoutEngine
from tic_tac_toe_detroix23 import (
    configurations, indexing, plays, conditions, graphs, ui, exports, optimization
)

EXCEPTIONS: tuple[Type[Exception], ...] = (TypeError, ValueError)

HELP: Final[str] = """
## Help.
"""

INPUT_YES: set[str] = {"", "y", "ye", "yes", "true", "1"}

_T_INPUT = TypeVar("_T_INPUT")

def get_input(
    input_type: Type[_T_INPUT],
    message: str,
    default: _T_INPUT,
    *,
    enable: bool = True,
) -> _T_INPUT:
    """
    Get user input and returns converted to `_T_INPUT`.
    """
    if not enable:
        return default

    options: str = input_type.__name__
    if issubclass(input_type, enum.Enum):
        options = " | ".join(input_type.__members__.keys()) 

    user_input: str = input(f"{message} [{options}]({default}): ")
    output: _T_INPUT

    if not user_input:
        output = default
    
    else:
        try:
            output = input_type(user_input)  # type: ignore[call-arg]
        
        except EXCEPTIONS:
            try:
                output = input_type[user_input.upper()]  # type: ignore

            except EXCEPTIONS:
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
    print("## Custom graph.")
    print("Inputs [options](default).\n")

    try:    
        player_count: int = get_input(int, "Player count", 2)
        player_start: int = get_input(int, "Starting player", 2)
        size: tuple[int, int] = (
            get_input(int, "Size X of the board", 3),
            get_input(int, "Size Y of the board", 3),
        )
        win_length: int = get_input(int, "Aligned length to win", 3)
        enable_draw: bool = input("Enable draw ? [y | n](y):").lower() in INPUT_YES
        print(f"=> `{enable_draw}`")
        layout_engine: LayoutEngine = get_input(
            LayoutEngine, 
            "Graphical engine", 
            LayoutEngine.PYVIS,
        )

        file_format: FileFormat
        if layout_engine not in {LayoutEngine.PYVIS}:
            file_format = get_input(FileFormat, "File format", FileFormat.SVG)
        else:
            file_format = FileFormat.SVG
        
        print(f"""
Global parameters:
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
            name: str = f"manual{node_start}_{size[0]}x{size[1]}_d{depth}"
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

            print(f"\nGraph node count: \n  q={len(graph)}")

            graph_index: indexing.GraphIndex = graphs.indexing(
                graph,
                node_start,
                player_start,
                player_count,
                win_conditions,
                depth_start=0,
            )
            
            print("(?) cli.draw_graph() `populate_forced_wins` Start.")
            time_populate_forced_wins: float = time.perf_counter()
            optimization.populate_forced_wins(
                node_start,
                graph_index,
                shift=1,
            )
            print(
                "(?) cli.draw_graph() `populate_forced_wins` End in "
                f"{time.perf_counter() - time_populate_forced_wins:.2f}s."
            )

            ## Collecting end states:
            end_states: dict[int, int] = graphs.outcomes(
                graph_index,
                player_count,
            )
            
            print("\nEnd states: ")
            for win_state, count in end_states.items():
                print(f"- {win_state}: {count};")

            print("\nNeighbor nodes outcomes: ")
            player_next: int = plays.next_player(player_start, player_count)
            next_best_node: int = optimization.next_best_node(
                node_start,
                graph,
                graph_index,
                player_start,
                player_count,
                method=optimization.NextBestNodeMethod.COUNT,
            )
            print(f"=> Next best for player i={player_next}: n={next_best_node}.")
                    
            # Exporting and graphing.
            print(f"\n### Outputs (as `{name}`).")

            exports.play_graph(
                f"ttt_{name}", 
                graph, 
                size, 
                1, 
                player_count,
                2
            )

            print("\nIndex: ")
            print("- " + "\n- ".join([
                f"{state}" 
                for state in graph_index.values()
            ]))

            print("\nDictionary: ")
            print(ui.format_graph(graph))


            if enable_draw:                
                graph_drawer: graphing.GraphDrawer

                if layout_engine == LayoutEngine.PYVIS:
                    graph_drawer = pyvis_wrapper.GraphDrawer(
                        name,
                        graph,
                        graph_index,
                        node_start,
                        player_start,
                        player_count,
                        size,
                        win_conditions
                    )
                
                else:
                    graph_drawer = graphviz_wrapper.GraphDrawer(
                        name,  
                        graph,
                        graph_index,
                        node_start,
                        player_start,
                        player_count,
                        win_conditions,
                        file_format,
                        layout_engine,
                    )
                
                graph_drawer.draw()

    except KeyboardInterrupt:
        print(f"\n(?) cli.draw_graph() Interrupted by CTRL+C.")

    return

def auto_optimum_plays() -> None:
    """
    Let the plays be chosen by the `optimization.next_best_node` automatically. 
    """
    print("## Auto-optimum play.\n")

    play: int = 0
    player_count: int = get_input(int, "Player count", 2)
    player: int = get_input(int, "Starting player", 1)
    size: tuple[int, int] = (
        get_input(int, "Size X of the board", 3),
        get_input(int, "Size Y of the board", 3),
    )
    win_length: int = get_input(int, "Aligned length to win", 3)
    node: int = get_input(int, "Node code", 0)
    board: Board = configurations.reverse_image(
        node,
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
        board,
        size,
        plays.next_player(player, player_count, -1),
        player_count,
        win_conditions,
    )
    graph_index: indexing.GraphIndex = graphs.indexing(
        graph,
        node,
        player,
        plays.next_player(player, player_count, 0),
        win_conditions,
        depth_start=0,
    )

    print()

    while not (
        win_conditions.is_win(node) 
        or graphs.is_leaf(graph, node)
    ):
        print(f"- Play {play}.")

        node = optimization.next_best_node(
            node,
            graph,
            graph_index,
            player,
            player_count,
            method=optimization.NextBestNodeMethod.RATIO,
        )
        board = configurations.reverse_image(
            node,
            player_count + 1,
            size[0] * size[1],
        )

        graph = plays.generate_graph(
            board,
            size,
            player,
            player_count,
            win_conditions,
        )
        graph_index = graphs.indexing(
            graph,
            node,
            player,
            player_count,
            win_conditions,
            depth_start=0,
        )

        print(f"Player i={player}, play n={node}, board: ")
        print(ui.format_board(board, size))

        play += 1
        player = plays.next_player(player, player_count)

    return
