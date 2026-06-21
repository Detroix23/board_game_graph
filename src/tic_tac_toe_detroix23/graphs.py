"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphs.py

Graph logic.
"""
from tic_tac_toe_detroix23.definitions import Graph

def depth_indexing(
    graph: Graph,
    node_start: int,
    depth_start: int = 0,

) -> list[tuple[int, int]]:
    """
    Similar to a breadth-first search, but returns a list of couples:
    - 0: node: `int`;
    - 1: depth: `int`
    """
    visited: set[int] = set()
    queue: list[tuple[int, int]] = [(node_start, depth_start)]
    depths: list[tuple[int, int]] = []

    while queue:
        node, depth = queue.pop(0)
        if node not in visited:
            visited.add(node)
            depths.append((node, depth))

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((int(neighbor), depth + 1))

    return depths
