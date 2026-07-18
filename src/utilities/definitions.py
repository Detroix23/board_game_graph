"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/definitions.py
"""
import enum
from typing import Final

DEFAULT_FILE_FORMAT: Final[str] = "svg"


class Tri(enum.Enum):
    """
    # Expended `bool` with a `NONE`.

    Attributes:
        `NONE`: -1;
        `FALSE`: 0;
        `TRUE`: 1;
    """
    NONE = -1
    """ `NONE`: acts as unknown, undefined, un-initialized. """
    FALSE = 0
    TRUE = 1

    def __bool__(self) -> bool:
        return self == Tri.TRUE

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"Tri.{self.name}"

    def __or__(self, other: 'Tri') -> 'Tri':
        """
        `or` operation with `NONE` (-1), `FALSE` (0), `TRUE` (1).

        |or    | -1| 0 | 1 |
        |--    | --| --| --|
        |**-1**| -1| -1|  1|
        |**0** | -1|  0|  1|
        |**1** |  1|  1|  1|

        """
        if self is Tri.TRUE:
            return self
        
        if self is Tri.FALSE:
            return other

        else:
            if other is Tri.TRUE:
                return other
            else:
                return Tri.NONE


class FileFormat(enum.Enum):
    """
    # `FileFormat` for exporting.
    """
    DEFAULT = 0
    SVG = 1
    PNG = 2
    
    def to_str(self) -> str:
        """
        Convert this enumeration to its `str` representation.
        """
        if self != FileFormat.DEFAULT:
            return self.name.lower()
        else:
            return DEFAULT_FILE_FORMAT
        
    def __str__(self) -> str:
        """
        Returns the readable name of an option.
        """
        return self.name