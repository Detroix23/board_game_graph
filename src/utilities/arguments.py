"""
# Board game graphing: utilities.
/src/board_games_maths/arguments.py
"""
from typing import Callable, Sequence

CalledFunction = Callable[[list[str], int], None] | Callable[[], None]
"""
Type union:
- `Callable[[list[str], int], None]`
- `Callable[[], None]`

## Parameters:
1. `list[str]`: CLI arguments;
2. `int`: parser index.
"""

class Token:
    """
    # Simple `Token` holding a token identifier, description, function.
    """
    tokens: set[str]
    function: CalledFunction
    description: str
    """ 
    Called when tokens matches. 
    
    ## Parameters:
    1. `list[str]`: CLI arguments;
    2. `int`: parser index.
    """

    def __init__(
        self, 
        tokens: set[str], 
        function: CalledFunction,
        description: str, 
    ) -> None:
        """
        Creates a `Token`.
        """
        self.tokens = tokens
        self.description = description
        self.function = function

        return
    
    def __str__(self) -> str:
        """
        Returns a described string of the `Token`.
        """
        tokens_sorted: list[str] = sorted(token for token in self.tokens)
        tokens_sorted.sort(key=len)

        return (
            f"- [{" | ".join(tokens_sorted)}] {self.function.__name__}()"
            f"\n\t{self.description}"
        )


class Parser:
    """
    # A `Parser` parsing command-line argument using `Token`s.
    """
    tokens: list[Token]
    path: str

    def __init__(self, tokens: list[Token]) -> None:
        """
        Instantiate a `Parser` with no tokens.
        """
        self.tokens = tokens
        self.path = ""

        return

    def parse(self, arguments: list[str]) -> None:
        """
        Parse by checking for each `arguments` if a `Token` matches.
        """
        for index, argument in enumerate(arguments):
            if index == 0:
                self.path = argument
                continue
            
            used: bool = False

            for token in self.tokens:
                if argument in token.tokens:
                    print(
                        "(?) utilities.arguments.Parser.parse() "
                        f"Argument `{argument}`: calling `{token.function.__name__}`."
                    )
                    used = True
                    exceptions: Sequence[Exception | None] = []

                    try:
                        token.function(arguments, index)  # type: ignore
                    except Exception as exception:
                        exceptions.append(exception)

                    try: 
                        token.function()  # type: ignore
                    except Exception as exception:
                        exceptions.append(exception)

                    if len(exceptions) == 2:
                        print(
                            "(!) utilities.arguments.Parser.parse() "
                            f"Failed: {len(exceptions)} exceptions raised:"
                        )
                        for exception in exceptions:
                            print(f"- {exception};") 
        
            if not used:
                print(
                    "\n(!) utilities.arguments.Parser.parse() "
                    f"Argument {index} unknown (`{argument}`)."
                )

        return
    
    def help_message(self) -> str:
        """
        Generate a formatted help string summing-up the `Token`s.
        """
        return "\n\n".join(str(token) for token in self.tokens)
