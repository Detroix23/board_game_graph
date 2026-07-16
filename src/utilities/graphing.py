"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/graphing.py
"""
import abc

class GraphDrawer(abc.ABC):
    """
    # Base class for all `GraphDrawer`s.
    """

    @abc.abstractmethod
    def populate(self) -> None:
        """
        Generate the visual by treating all nodes.
        """
        ...

    @abc.abstractmethod
    def draw(self) -> None:
        """
        Display the graph.
        """
        ...
    