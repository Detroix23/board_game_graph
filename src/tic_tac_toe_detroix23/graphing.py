# type: ignore
"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphing.py

Draw graphs with `graphviz`.
"""
import graphviz

from tic_tac_toe_detroix23.definitions import Graph, PATH_GRAPH


def draw(
    name: str, 
    graph: Graph
) -> graphviz.Digraph:
    """
    Draw a with `graphviz` the `graph`.
    """
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
        dot.node(str(node))
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dot.edge(str(node), str(neighbor))
    
    dot.render(
        filename=f"ttt_{name}.dot",
        directory=str(PATH_GRAPH), 
        format="svg",
        view=True,
    ) 

    return dot
