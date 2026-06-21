"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphing.py

Draw graphs with `graphviz`.
"""
import time

import graphviz  # pyright: ignore[reportMissingTypeStubs]

from tic_tac_toe_detroix23.definitions import Graph, PATH_GRAPH
from tic_tac_toe_detroix23 import conditions

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
    Basic: all node are the same
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

    print(f"(?) graphing.draw(name={name}) End in {time.perf_counter() - time_start}s.")
    return dot

def draw(
    name: str, 
    graph: Graph,
    node_start: int,
    player_start: int,
    player_count: int,
    win_conditions: conditions.WinConditions,
) -> graphviz.Digraph:
    """
    Draw a with `graphviz` the `graph`.
    Style:
    - squared are win. 
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


    # Breadth-first explore.
    depth_start: int = 0
    visited: set[int] = set()
    queue: list[tuple[int, int]] = [(node_start, depth_start)]

    while queue:
        node, depth = queue.pop(0)
        if node not in visited:
            visited.add(node)
            
            # Node configuration.
            shape: str = "circle"
            if win_conditions.is_win(node):
                # Win.
                shape = "box"
            elif len(graph.get(node, [])) == 0:
                # Leaf.
                shape = "egg"

            dot.node(  # pyright: ignore[reportUnknownMemberType]
                str(node),
                shape=shape,
                fillcolor=hsv(
                    ((depth + player_start - 1) % player_count) / (player_count + 1), 
                    0.9, 
                    0.9,
                ),
            )

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((int(neighbor), depth + 1))

    # Linking.
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dot.edge(  # pyright: ignore[reportUnknownMemberType]
                str(node), 
                str(neighbor),
            )
    
    dot.render(  # pyright: ignore[reportUnknownMemberType]
        filename=f"ttt_{name}.neato.dot",
        directory=str(PATH_GRAPH), 
        format="svg",
        view=True,
    ) 

    print(f"(?) graphing.draw(name={name}) End in {time.perf_counter() - time_start}s.")
    return dot
