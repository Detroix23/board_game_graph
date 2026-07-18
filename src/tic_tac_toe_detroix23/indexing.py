"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/indexing.py
"""
from typing import Optional

from utilities.definitions import Tri
from tic_tac_toe_detroix23.definitions import ImageList


GraphIndex = dict[int, 'NodeState']
""" A detailed view of all nodes of a graph. """

class NodeState:
    """
    # Named tuple to index `NodeState`s of a graph.
    Used in `GraphIndex` to give a information-full representation of a graph.
    
    Attributes:
        `node`: `int` 
        `depth`: `int`
        `win_state`: `int`
        `neighbors`: `Optional[ImageList]`
        `forced_win`: `bool`
    """
    node: int
    depth: int
    player: int
    win_state: int
    neighbors: Optional[ImageList]
    forced_win: Tri
    """ Tells if node's neighbors are all win for `player`. """

    def __init__(
        self,
        node: int,
        depth: int,
        player: int,
        win_state: int,
        neighbors: Optional[ImageList],
        forced_win: Tri = Tri.NONE,
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
        self.player = player
        self.win_state = win_state
        self.neighbors = neighbors
        self.forced_win = forced_win
        
        return
    
    def __str__(self) -> str:
        """
        Nice `NodeState` string representation of all the attributes.
        """
        return (
            f"node={self.node: <5} depth={self.depth} player={self.player} "
            f"win_state={self.win_state: <2} neighbors={self.neighbors} "
            f"forced_win={self.forced_win} "
        )

    def is_leaf(self) -> bool:
        """
        Returns if the `NodeState` has no neighbors.
        """
        return self.neighbors is None or len(self.neighbors) == 0

    def is_winning(self) -> bool:
        """
        Returns if the position is a win.
        """
        return self.win_state > 0
