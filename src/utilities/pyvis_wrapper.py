"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/pyvis_wrapper.py

Draw graphs with `pyvis`.
"""
import pathlib

import pyvis  # pyright: ignore[reportMissingTypeStubs]

from utilities import graphics
from tic_tac_toe_detroix23.definitions import Graph, PLAYER_SYMBOLS, PATH_PYVIS
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
            height="85vh",
            width="100vw",
            directed=True,
            notebook=False,
            select_menu=True,      
            cdn_resources="remote", 
        )

        self.populate()

        return
    
    def populate(self) -> None:
        """
        Update `pyvis`' `Network` from `self` `graph` (`dict`).
        """
        player_symbols: list[str] = PLAYER_SYMBOLS
        player_symbols[0] = "_"

        # Nodes.
        for node, state in self.graph_index.items():
            shape: str = "circle"
            scale: int = max(1, len(self.graph.get(node, [])))
            additional_settings: dict[str, int] = {}
            if state.win_state > 0:
                shape = "box"
            elif state.win_state == 0:
                shape = "ellipse"
            elif node == self.node_start:
                shape = "star"
                additional_settings |= {
                    "x": 0, 
                    "y": 0, 
                    "physics": False
                }

            self.network.add_node(  # pyright: ignore[reportUnknownMemberType]
                node,
                label=str(node),
                title=ui.format_board(
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
                ),
                color="#"+graphics.hsv_to_rgb_hex(
                    state.player / self.player_count, 
                    0.9, 
                    0.9,
                ),
                shape=shape,
                value=scale * 60,
                size=scale * 60,
                **additional_settings,
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
        path: pathlib.Path = PATH_PYVIS / f"ttt_{self.name}.html"
        print(str(path))

        self.network.toggle_physics(True)  # pyright: ignore[reportUnknownMemberType]
        self.network.show_buttons()         # pyright: ignore[reportUnknownMemberType]
        self.network.show(                  # pyright: ignore[reportUnknownMemberType]
            name=str(path),
            notebook=False,
        )

        return
