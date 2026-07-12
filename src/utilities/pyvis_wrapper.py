"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/pyvis_wrapper.py

Draw graphs with `pyvis`.
"""
import pyvis  # pyright: ignore[reportMissingTypeStubs]

from tic_tac_toe_detroix23.definitions import Graph, PLAYER_SYMBOLS
from tic_tac_toe_detroix23 import configurations, conditions, graphs, ui

class GraphDrawer:
    """
    # Complete `GraphDrawer` with `graphviz`.
    """
    name: str
    graph: Graph
    graph_index: graphs.GraphIndex
    node_start: int
    player_start: int
    player_count: int
    size: tuple[int, int]
    win_conditions: conditions.WinConditions
    
    network: pyvis.network.Network

    def __init__(
        self,
        name: str, 
        graph: Graph,
        graph_index: graphs.GraphIndex,
        node_start: int,
        player_start: int,
        player_count: int,
        size: tuple[int, int],
        win_conditions: conditions.WinConditions,
    ) -> None:
        """
        Instantiate a `GraphDrawer` and the `dot`. Does not draw the graph.
        """
        self.name = name
        self.graph = graph
        self.graph_index = graph_index
        self.node_start = node_start
        self.player_start = player_start
        self.player_count = player_count
        self.size = size
        self.win_conditions = win_conditions
        self.network = pyvis.network.Network(
            directed=True,
            notebook=False,
            select_menu=True,       
        )

        self.update_from_graph()

        return
    
    def update_from_graph(self) -> None:
        """
        Update `pyvis`' `Network` from `self` `graph` (`dict`).
        """
        player_symbols: list[str] = PLAYER_SYMBOLS
        player_symbols[0] = "_"

        # Nodes.
        nodes: list[int] = [int(node) for node in set(self.graph.keys()
            ).union(*[
                set(neighbors.tolist()) 
                for neighbors in self.graph.values()
            ])
        ]

        print(type(nodes[0]))

        self.network.add_nodes(  # pyright: ignore[reportUnknownMemberType]
            nodes,
            label=[str(node) for node in nodes],
            title=[
                ui.format_board(
                    configurations.reverse_image(
                        node, 
                        self.player_count + 1, 
                        self.size[0] * self.size[1]
                    ),
                    self.size,
                    horizontal="",
                    intersection="",
                    lines="",
                    player_symbols=player_symbols,
                ) 
                for node in nodes
            ],
        )

        # Edges.
        for node, neighbors in self.graph.items():
            self.network.add_edges([  # pyright: ignore[reportUnknownMemberType]
                (int(node), int(neighbor))
                for neighbor in neighbors
            ])

        return

    def draw(self) -> None:
        """
        Draw a with `pyvis` the `graph`.
        """
        self.network.show(  # pyright: ignore[reportUnknownMemberType]
            name=f"ttt_{self.name}.html",
            local=True,
            notebook=False,
        )

        return
