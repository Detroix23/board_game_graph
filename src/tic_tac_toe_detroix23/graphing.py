"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphing.py

Draw graphs with `graphviz`.
"""
import time

import graphviz  # pyright: ignore[reportMissingTypeStubs]

from tic_tac_toe_detroix23.definitions import Graph, PATH_GRAPH, FileFormat, LayoutEngine
from tic_tac_toe_detroix23 import conditions, graphs

def hsv(hue: float, saturation: float, value: float) -> str:
    """
    Format a `hsv` color to `str` for `graphviz`.
    """
    return f"{hue:.3f} {saturation:.3f} {value:.3f}"

def draw_basic(
    name: str, 
    graph: Graph,
) -> graphviz.Digraph:
    """
    Draw a with `graphviz` the `graph`.
    Basic: all node are the same.
    """
    print(f"(?) graphing.draw(name={name}) Start...")
    time_start: float = time.perf_counter()

    dot: graphviz.Digraph = graphviz.Digraph(
        name, 
        comment="Tic-Tac-Toe.",
        engine="neato",
        strict=True,
        format="svg",
        graph_attr={
            "splines": "true",
            "overlap": "false"
        },
    )

    for node in graph:
        dot.node(str(node))  # pyright: ignore[reportUnknownMemberType]
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dot.edge(  # pyright: ignore[reportUnknownMemberType]
                str(node), 
                str(neighbor)
            )
    
    dot.render(  # pyright: ignore[reportUnknownMemberType]
        filename=f"ttt_{name}.neato.dot",
        directory=str(PATH_GRAPH), 
        format="svg",
        view=True,
    ) 

    time_elapsed: float = time.perf_counter() - time_start
    print(f"(?) graphing.draw(name={name}) End in {time_elapsed:.2f}s.")
    return dot

class GraphDrawer:
    """
    # Complete `GraphDrawer` with `graphviz`.
    """
    name: str
    graph: Graph
    graph_index: dict[int, graphs.NodeState]
    node_start: int
    player_start: int
    player_count: int
    win_conditions: conditions.WinConditions
    format: FileFormat
    layout_engine: LayoutEngine
    
    dot: graphviz.Digraph

    def __init__(
        self,
        name: str, 
        graph: Graph,
        graph_index: dict[int, graphs.NodeState],
        node_start: int,
        player_start: int,
        player_count: int,
        win_conditions: conditions.WinConditions,
        format: FileFormat = FileFormat.DEFAULT,
        layout_engine: LayoutEngine = LayoutEngine.DEFAULT,
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
        self.win_conditions = win_conditions
        self.format = format
        self.layout_engine = layout_engine

        self.dot: graphviz.Digraph = graphviz.Digraph(
            self.name, 
            comment=f"Tic-Tac-Toe play-graph. Start={self.node_start}",
            engine=self.layout_engine.to_str(),
            strict=True,
            format=self.format.to_str(),
            graph_attr={
                "splines": "true",
                "overlap": "false",
                "bgcolor": "white",
            },
            node_attr={
                "style": "filled",
                "fillcolor": "white",
                "color": "black",
                "arrowhead": "diamond",
                "shape": "circle",
                "width": "0.69",
                "fixedsize": "true",
            }
        )
        return

    def add_node(
        self,
        node_state: graphs.NodeState,
    ) -> None:
        """
        Node configuration to add to `dot`.
        Style:
        - colors: 1='red', 2='cyan'; 
        - 'circle' is normal;
        - 'box' is a win;
        - 'egg' is a leaf.
        """ 
        shape: str = "circle"
        if node_state.win_state > 0:
            shape = "box"
        elif node_state.win_state == 0:
            shape = "egg"

        self.dot.node(  # pyright: ignore[reportUnknownMemberType]
            str(node_state.node),
            shape=shape,
            fillcolor=hsv(
                (
                    ((node_state.depth + self.player_start - 1) % self.player_count) 
                    / self.player_count
                ), 
                0.9, 
                0.9,
            ),
        )
        return

    def render(self) -> None:
        """
        Render the `dot`.
        """
        self.dot.render(  # pyright: ignore[reportUnknownMemberType]
            filename=f"ttt_{self.name}.{self.layout_engine.to_str()}.dot",
            directory=str(PATH_GRAPH), 
            format="svg",
            view=True,
        ) 

    def draw(self) -> graphviz.Digraph:
        """
        Draw a with `graphviz` the `graph`.

        Style:
        - colors: 1='red', 2='cyan'; 
        - 'circle' is normal;
        - 'box' is a win;
        - 'egg' is a leaf.
        """
        print(f"(?) graphing.draw(name={self.name}) Start...")
        time_start: float = time.perf_counter()

        # Breadth-first explore.
        for node_state in self.graph_index.values():
            self.add_node(node_state)
        
        # Linking.
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                self.dot.edge(  # pyright: ignore[reportUnknownMemberType]
                    str(node), 
                    str(neighbor),
                )

        self.render()

        time_elapsed: float = time.perf_counter() - time_start
        print(f"(?) graphing.draw(name={self.name}) End in {time_elapsed:.2f}s.")
        return self.dot
