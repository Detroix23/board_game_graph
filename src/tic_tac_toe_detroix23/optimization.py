"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/optimization.py
"""
import enum

from tic_tac_toe_detroix23.definitions import Graph
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
    graph_index: graphs.GraphIndex,
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
                f"node={starting_neighbors: <5} ratio={ratio}, "
                f"outcomes={outcomes} c={outcomes_count};"
            ))

    print("\n".join([
        f"{'*' if node == best_node else '-'} {message}"
        for node, message in nodes   
    ]))

    return best_node
