"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/optimization.py
"""
import enum


from utilities.definitions import Tri
from utilities.debug import debug_print, assert_neq
from tic_tac_toe_detroix23.definitions import Graph
from tic_tac_toe_detroix23.indexing import GraphIndex, NodeState
from tic_tac_toe_detroix23 import graphs

class NextBestNodeMethod(enum.Enum):
    """
    # `NextBestNodeMethod` for `next_best_node` algorithm.
    """
    COUNT = 0
    RATIO = 1


def next_best_node(
    starting_node: int,
    graph: Graph,
    graph_index: GraphIndex,
    player: int,
    player_count: int,
    method: NextBestNodeMethod = NextBestNodeMethod.COUNT,
) -> int:
    """
    Take all sub-graphs (neighbors nodes, next plays) from `graph`,
    and choose the best move for `player` counting the `outcomes` from `graph_index`. 
    """
    print(
        "(?) optimization.next_best_node("
        f"starting_node={starting_node}, player={player}, method={method.name}) Start."
    )

    best_node: int = 0
    best_score: float = 0.0

    # Nodes and debug message.
    nodes: list[tuple[int, str]] = []

    for starting_neighbors in graph[starting_node]:
        _, sub_index = graphs.sub_graph(
            graph,
            graph_index,
            int(starting_neighbors),
        )

        outcomes: dict[int, int] = graphs.outcomes(sub_index, player_count)

        if method == NextBestNodeMethod.COUNT:
            wins: int = outcomes[player]
            if wins >= best_score:
                best_node = int(starting_neighbors)
                best_score = wins

            nodes.append((
                int(starting_neighbors), 
                f"node={starting_neighbors: <5} wins={wins: <2} outcomes={outcomes};")
            )

        elif method == NextBestNodeMethod.RATIO:
            outcomes_count: int = sum(
                {
                    player: count 
                    for player, count in outcomes.items()
                    if player >= 0
                }.values()
            )
            ratio: float = outcomes[player] / outcomes_count
            if ratio >= best_score:
                best_node = int(starting_neighbors)
                best_score = ratio

            nodes.append((
                int(starting_neighbors),
                f"node={starting_neighbors: <5} ratio={ratio} "
                f"outcomes={outcomes} c={outcomes_count};"
            ))

    print("\n".join([
        f"{'*' if node == best_node else '-'} {message}"
        for node, message in nodes   
    ]))

    return best_node


def populate_forced_wins(
    node: int,
    graph_index: GraphIndex,
    debug: bool = False,
    *,
    shift: int = 0,
) -> None:
    """
    Update the `graph_index` to find recursively forced wins.

    Looks for `node` if it exists a forced win 
    for all combinations of plays of the opponents.

    **Arguments**:
    - `node`: `int`,
    - `graph_index`: `GraphIndex`,
    - `short_circuit`: `bool`, allows the neighbors loop to be broken.
        - it allows faster check for `node`;
        - but does not ensure that all nodes are checked.
    
    **Todo**:
    - `shift` is currently limited to `0` and `1`.
    - depth-search only available for 2 players.
    """
    def body(
        node: int,
        graph_index: GraphIndex,
        debug: bool,
    ) -> Tri:
        """
        `populate_forced_win` recursive body.
        """
        state: NodeState = graph_index[node]
        debug_print(f"(?) graphs.populate_forced_wins(node={node}) Start.", debug)

        if (
            state.neighbors is None 
            or state.is_leaf()
        ):
            # Base case: leaf.
            state.forced_win = (
                Tri.TRUE
                if state.is_winning()
                else Tri.FALSE
            )

            debug_print(
                f"(?) graphs.populate_forced_wins(node={node}) "
                f"End in base-case with {state.forced_win}.",
                debug,
            )
            return state.forced_win

        else:
            # Recursion.
            forced: Tri = Tri.TRUE

            # 2-nested loop: only for 2 players.
            for neighbor1 in state.neighbors:
                state1: NodeState = graph_index[int(neighbor1)]
                forced1: Tri = Tri.FALSE

                if state1.neighbors is not None:
                    for neighbor2 in state1.neighbors:
                        state2: NodeState = graph_index[int(neighbor2)]
                        # Recurse if not initialized (`NONE`).
                        if state2.forced_win == Tri.NONE:
                            state2.forced_win = body(
                                node=int(neighbor2),
                                graph_index=graph_index,
                                debug=debug,
                            )
                        
                        assert_neq(state2.forced_win, Tri.NONE)
                        forced1 |= state2.forced_win

                forced &= forced1

            state.forced_win = forced
            debug_print(
                f"(?) graphs.populate_forced_wins(node={node}) "
                f"End with {forced}.",
                debug,
                flush=True,
            )
            assert_neq(forced, Tri.NONE)
            return forced

    state: NodeState = graph_index[node]
    if shift == 1 and state.neighbors is not None:
        for neighbor in state.neighbors:
            body(int(neighbor), graph_index, debug)    

    else:
        body(node, graph_index, debug)

    return
