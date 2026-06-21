"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphs.py

Graph logic.
"""
import numpy

from tic_tac_toe_detroix23.definitions import Graph
from tic_tac_toe_detroix23.conditions import WinConditions
from tic_tac_toe_detroix23 import plays

GraphIndex = dict[int, 'NodeState']

class NodeState:
    """
    # Named tuple to index `NodeState`s of a graph.
    """
    node: int
    depth: int
    win_state: int
    """ 
    - `0`: game ending with a tie;
    - `> 0`: winning player's ID;
    - `-1`: else.
    """
    def __init__(
        self,
        node: int,
        depth: int,
        win_state: int,
    ) -> None:
        """
        Create the named tuple `NodeState`.

        `win_state`:
        - `0`: game ending with a tie;
        - `> 0`: winning player's ID;
        - `-1`: else.
        """
        self.node = node
        self.depth = depth
        self.win_state = win_state
        
        return

def is_leaf(
    graph: Graph,
    node: int
) -> bool:
    """
    Returns if `node` is a leaf of `graph`. 
    """
    return len(graph.get(node, [])) == 0

def set_win_state(
    graph: Graph,
    node: int,
    player: int,
    win_conditions: WinConditions
) -> int:
    """
    Returns an `int` corresponding to the `win_state` of `node` in `graph`:
    - `0`: game ending with a tie;
    - `> 0`: winning player's ID;
    - `-1`: else.
    """
    state: int = -1
    if win_conditions.is_win(node):
        state = player
    elif is_leaf(graph, node):
        state = 0

    return state

def indexing(
    graph: Graph,
    node_start: int,
    player_start: int,
    player_count: int,
    win_conditions: WinConditions,
    depth_start: int = 0,
) -> GraphIndex:
    """
    Use a breadth-first search, to return a `dict` of `node`: `NodeState`:
    - node: `int`;
    - depth: `int`;
    - win_state: `int`. 
    """
    node_start_win_state: int = set_win_state(
        graph,
        node_start,
        player_start,
        win_conditions
    )

    visited: set[int] = set()
    queue: list[NodeState] = [NodeState(
        node_start, 
        depth_start, 
        node_start_win_state
    )]
    index: dict[int, NodeState] = dict()

    while queue:
        state: NodeState = queue.pop(0)
        if state.node not in visited:
            visited.add(state.node)
            index[state.node] = (NodeState(
                state.node, 
                state.depth,
                state.win_state
            ))

            for neighbor in graph.get(state.node, []):
                if neighbor not in visited:
                    player: int = plays.turn_player(
                        state.depth + 1, 
                        player_start, 
                        player_count,
                    )
                    
                    queue.append(NodeState(
                        int(neighbor), 
                        state.depth + 1,
                        set_win_state(
                            graph,
                            int(neighbor),
                            player,
                            win_conditions
                        )
                    ))

    return index

def outcomes(
    graph_index: dict[int, NodeState],
    player_count: int,
) -> dict[int, int]:
    """
    Count all outcomes, `win_states`, of the `graph`.
    """
    counter: dict[int, int] = {
        index: 0 for index in range(-1, player_count + 1)
    }

    for node_state in graph_index.values():
        counter[node_state.win_state] += 1

    return counter

def sub_graph(
    source: Graph,
    source_index: GraphIndex,
    node: int,
) -> tuple[Graph, GraphIndex]:
    """
    Individuates the sub-graph from `node` of `source`.

    Returns a couple:
    - 0: the new sub-graph;
    - 1: sub-graph's index.
    """
    visited: set[int] = set()
    queue: list[int] = [node]
    sub_graph: Graph = dict()
    sub_index: GraphIndex = dict()

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            # Copying.
            sub_graph[node] = source.get(
                node, 
                numpy.empty((0,), dtype=numpy.uint32
            ))
            sub_index[node] = source_index[node]

            for neighbor in source.get(node, []):
                if neighbor not in visited:
                    queue.append(int(neighbor))

    return (sub_graph, sub_index)
