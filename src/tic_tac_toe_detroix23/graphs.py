"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/graphs.py

Graph logic.
"""
from tic_tac_toe_detroix23.definitions import Graph
from tic_tac_toe_detroix23.conditions import WinConditions
from tic_tac_toe_detroix23 import plays

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
) -> list[NodeState]:
    """
    Use a breadth-first search, to return a `list` of `NodeState`:
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
    depths: list[NodeState] = []

    while queue:
        state: NodeState = queue.pop(0)
        if state.node not in visited:
            visited.add(state.node)
            depths.append(NodeState(
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

    return depths
