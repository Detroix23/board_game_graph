"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/graphics.py
"""

def hsv(hue: float, saturation: float, value: float) -> str:
    """
    Format a `hsv` color to `str` for `graphviz`.
    """
    return f"{hue:.3f} {saturation:.3f} {value:.3f}"
