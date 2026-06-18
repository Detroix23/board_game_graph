"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/definitions.py

Constant and hard-coded values.
"""

from typing import Final, TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe_detroix23.configurations import Configuration

Graph = dict['Configuration', list['Configuration']]
