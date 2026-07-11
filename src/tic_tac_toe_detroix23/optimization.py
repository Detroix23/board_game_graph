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
    print(f"(?) optimization.next_best_node() Start n=`{starting_node}`, with method `{method.name}`.")

    best_node: int = 0
    best_score: float = 0.0

    for node in graph[starting_node]:
        _sub, sub_index = graphs.sub_graph(
            graph,
            graph_index,
            int(node),
        )

        outcomes: dict[int, int] = graphs.outcomes(sub_index, player_count)

        if method == NextBestNodeMethod.COUNT:
            wins: int = outcomes[player]
            if wins >= best_score:
                best_node = int(node)
                best_score = wins

            print(f"- node={node}, wins={wins}, outcomes={outcomes};")

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
                best_node = int(node)
                best_score = ratio

            print(
                f"- node={node}, ratio={ratio}, "
                f"outcomes={outcomes}, c={outcomes_count};"
            )

    return best_node
