"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/cli.py
"""
from typing import Final

from tic_tac_toe_detroix23 import configurations, ui

HELP: Final[str] = """
## Help.

CLI arguments:
- "h", "help":
    Prints this help.

- "t", "assertions":
    tests.configurations1()
    tests.next_configuration1()

- "tbg1":
    tests.generate_board_graph1()

- "tbg2":
    tests.generate_board_graph2()

- "twc1":
    tests.win_conditions1()

- "r", "reverse":
    cli.reverse_image()

"""

def reverse_image() -> None:
    """
    Input loop to convert input `code` to a board.
    """
    print("## Reverse image.\n")
    player_count: int = 2
    size: tuple[int, int] = (3, 3)
    print(f"""With:
- player_count={player_count};
- size={size}.
""")
    try: 
        while True:
            code: str = input("\ncode: ")
            print(ui.format_board(configurations.reverse_image(
                int(code),
                player_count + 1,
                size[0] * size[1],
            ), size))
    except KeyboardInterrupt as interrupt:
        print(f"\nInterrupted by CTRL+C. Details: \n```\n{interrupt}\n```\n")

    return

