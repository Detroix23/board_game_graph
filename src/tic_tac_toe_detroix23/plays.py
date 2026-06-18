"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/plays.py
"""

from tic_tac_toe_detroix23.definitions import Graph
from tic_tac_toe_detroix23.configurations import Configuration


def generate_plays_graph(root: Configuration, depth: int) -> Graph:
    """
    Recursively discovers and maps the `Graph`:
    - starting from `root`;
    - for many `depth` steps.
    """
    ...

def next_configurations(
    configuration: Configuration,
    player: int,
) -> list[Configuration]:
    """
    Returns all possible `Configuration` after the turn of `player`. 
    """
    ...