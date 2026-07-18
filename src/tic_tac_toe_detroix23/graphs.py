"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphs.py

Graph logic.
"""
from tic_tac_toe_detroix23.definitions import Graph, NULL_IMAGE_LIST
from tic_tac_toe_detroix23.indexing import GraphIndex, NodeState
from tic_tac_toe_detroix23.conditions import WinConditions
from tic_tac_toe_detroix23 import plays


def is_leaf(
    graph: Graph,
    node: int
) -> bool:
    """
    Returns if `node` is a leaf of `graph`. 
    Used to determine ties or end of graph.
    """
    return len(graph.get(node, [])) == 0

def determine_win_state(
    graph: Graph,
    node: int,
    win_conditions: WinConditions
) -> int:
    """
    Returns an `int` corresponding to 
    the `win_state` of `node` in `graph`:
    - `= 0`: game ending with a tie;
    - `> 0`: winning player's ID;
    - `= -1`: else.
    """
    winner: int = win_conditions.get_winner(node)
    return (
        winner
        if winner > 0 or not is_leaf(graph, node)
        else 0
    )

def indexing(
    graph: Graph,
    node_start: int,
    player_start: int,
    player_count: int,
    win_conditions: WinConditions,
    depth_start: int = 0,
) -> GraphIndex:
    """
    Uses a breadth-first search.
     
    Returns:
       `GraphIndex`: a `dict` of:
        - key: `int`, node ID;
        - value: :py:class:`NodeState`.

    Arguments:
        `graph`: `Graph`;
        `node_start`: `int`;
        `player_start`: `int`;
        `player_count`: `int`;
        `win_conditions`: `WinConditions`;
        `depth_start`: `int`. Used in recursion. Default `d = 0`;
    """
    visited: set[int] = set()
    index: dict[int, NodeState] = dict()
    queue: list[NodeState] = [NodeState(
        node_start, 
        depth_start, 
        player_start,
        win_state=determine_win_state(
            graph,
            node_start,
            win_conditions,
        ),
        neighbors=graph[node_start],
    )]

    while queue:
        state: NodeState = queue.pop(0)
        if state.node not in visited:
            # Register the unvisited node.
            visited.add(state.node)
            index[state.node] = (NodeState(
                state.node, 
                state.depth,
                state.player,
                state.win_state,
                neighbors=(
                    graph[state.node]
                    if state.node in graph.keys()
                    else None
                ),
            ))

            # Queue neighbors of the unvisited node.
            for neighbor in graph.get(state.node, []):
                if neighbor not in visited:
                    image: int = int(neighbor)
                    player: int = plays.turn_player(
                        state.depth + 1, 
                        player_start, 
                        player_count,
                    )

                    queue.append(NodeState(
                        node=image, 
                        depth=state.depth + 1,
                        player=player,
                        win_state=determine_win_state(
                            graph,
                            image,
                            win_conditions,
                        ),
                        neighbors=(   
                            graph[int(neighbor)]
                            if image in graph.keys()
                            else None
                        ),
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
        index: 0 
        for index in range(-1, player_count + 1)
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
    sub_graph: Graph = dict()
    sub_index: GraphIndex = dict()
    queue: list[int] = [node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            # Copying and treating the unvisited node.
            visited.add(node)
            sub_graph[node] = source.get(
                node, 
                NULL_IMAGE_LIST.copy(),  
            )
            sub_index[node] = source_index[node]

            # Queue unvisited node's neighbors.
            for neighbor in source.get(node, []):
                if neighbor not in visited:
                    queue.append(int(neighbor))

    return (sub_graph, sub_index)
