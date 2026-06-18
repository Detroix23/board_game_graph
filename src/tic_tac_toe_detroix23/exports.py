"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/exports.py
"""
import json

import numpy 

from tic_tac_toe_detroix23.definitions import Graph, PATH_GRAPH

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, o: object) -> object:
        encoded: object
        if isinstance(o, numpy.ndarray):
            encoded = o.tolist()
        else:
            encoded = json.JSONEncoder.default(self, o)
        
        return encoded

def export_play_graph(
    name: str,
    graph: Graph,
    size: tuple[int, int],
    player: int,
    player_count: int,
    depth: int,
) -> None:
    """
    Write the `graph` in JSON.
    """
    data: dict[str, object] = {
        "size": {
            "x": size[0],
            "y": size[1], 
        },
        "player_start": player,
        "player_count": player_count,
        "graph_depth": depth,
        "graph_nodes": len(graph),
        "graph": graph, 
    } 

    try:
        with open(PATH_GRAPH / f"{name.strip()}.json", "w") as json_file:
            json.dump(
                data, 
                json_file, 
                cls=NumpyArrayEncoder,
                indent=2,
            )
    except FileNotFoundError as file_not_found:
        print("(!) plays.export_play_graph() File not found:")
        print(f"```\n{file_not_found}\n```\n")

    return

