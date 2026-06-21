"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/__main__.py
"""
import sys

from tic_tac_toe_detroix23 import cli, tests

def argument_decider(arguments: list[str]) -> None:
    """
    Decides what to execute from `arguments`.
    """
    if len(arguments) < 2:
        print(f"(!) Not enough arguments (args:{arguments}).\n")
        print(cli.HELP)
        return

    mode: str = arguments[1]

    if mode in {"h", "help"}:
        print(cli.HELP)

    elif mode in {"t", "assertions"}:
        tests.configurations1()
        tests.next_configuration1()

    elif mode in {"tbg1",}:
        tests.generate_board_graph1()

    elif mode in {"tbg2",}:
        tests.generate_board_graph2()
    
    elif mode in {"twc1",}:
        tests.win_conditions1()

    elif mode in {"r", "reverse"}:
        cli.reverse_image()

    elif mode in {"g", "graph"}:
        cli.draw_graph()
        
    else:
        print(f"\n(!) Argument 1 `mode` unknown (`{mode}`).\n")
        print(cli.HELP)

    return

def main() -> None:
    """
    Main entry point for `tic_tac_toe_detroix23`.
    """
    print("\n# Board game graphing.\n")

    argument_decider(sys.argv)

    print("\n(?) End.")
    return

main()
