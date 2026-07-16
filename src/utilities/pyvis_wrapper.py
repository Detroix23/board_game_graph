"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/pyvis_wrapper.py

Draw graphs with `pyvis`.
"""
import pathlib

import pyvis  # type: ignore[import-untyped]

from utilities import graphics, graphing
from tic_tac_toe_detroix23.definitions import Graph, PLAYER_SYMBOLS, PATH_PYVIS
from tic_tac_toe_detroix23 import configurations, conditions, graphs, ui

class Shape:
    """
    # `pyvis`'s node `Shape`s.

    https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node
    
    Text inside:
    - ellipse, 
    - circle, 
    - database, 
    - box, 
    - text. 
    
    Text outside:
    - image, 
    - circularImage, 
    - diamond, 
    - dot, 
    - star, 
    - triangle, 
    - triangleDown, 
    - square
    - icon.
    """
    ELLIPSE = "ellipse"
    """ Text inside. """
    CIRCLE = "circle" 
    """ Text inside. """
    DATABASE = "database" 
    """ Text inside. """
    BOX = "box" 
    """ Text inside. """
    TEXT = "text" 
    """ Text inside. """
    IMAGE = "image" 
    """ Text outside. """
    IMAGE_CIRCULAR = "circularImage" 
    """ Text outside. """
    DIAMOND = "diamond" 
    """ Text outside. """
    DOT = "dot" 
    """ Text outside. """
    STAR = "star" 
    """ Text outside. """
    TRIANGLE = "triangle" 
    """ Text outside. """
    TRIANGLE_DOWN = "triangleDown" 
    """ Text outside. """
    SQUARE = "square"
    """ Text outside. """
    ICON = "icon"
    """ Text outside. """


class GraphDrawer(graphing.GraphDrawer):
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
            # Normal shape.
            shape: str = Shape.DOT
            scale: int = max(1, len(self.graph.get(node, [])))
            additional_settings: dict[str, int] = {}
            if state.win_state > 0:
                # Win.
                shape = Shape.SQUARE
            elif state.win_state == 0:
                # Tie.
                shape = Shape.TRIANGLE
            elif node == self.node_start:
                # Start.
                shape = Shape.STAR
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
                    (state.player - 1) / self.player_count, 
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

        self.network.toggle_physics(True)       # pyright: ignore[reportUnknownMemberType]
        self.network.toggle_drag_nodes(True)    # pyright: ignore[reportUnknownMemberType]
        self.network.toggle_stabilization(True) # pyright: ignore[reportUnknownMemberType]
        self.network.show_buttons()             # pyright: ignore[reportUnknownMemberType]
        print("Pyvis HTML export path:", end=" ")
        self.network.show(                      # pyright: ignore[reportUnknownMemberType]
            name=str(path),
            notebook=False,
        )

        return
