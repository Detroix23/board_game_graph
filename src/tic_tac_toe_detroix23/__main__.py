"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/__main__.py
"""
import sys

from utilities.arguments import Parser, Token
from tic_tac_toe_detroix23 import cli, tests

def argument_decider(arguments: list[str]) -> None:
    """
    Decides what to execute from `arguments`.
    """
    def print_help() -> None:
        """
        Prints CLI help using parser auto-generated help.
        """
        print(cli.HELP + parser.help_message())
        return

    parser = Parser(tokens=[
        Token({"t", "assertions"}, tests.general_assertions, "Run a global health-check."),
        Token({"tbg1",}, tests.generate_board_graph1, "Test board with preset 1."),
        Token({"tbg2",}, tests.generate_board_graph2, "Test board with preset 2."),
        Token({"twc1",}, tests.win_conditions1, "Test win conditions."),
        Token(
            {"r", "reverse"}, cli.reverse_image, 
            "Dialog to find the reverse image of a given `int` code",
        ),
        Token(
            {"g", "graph"}, cli.draw_graph, 
            "Dialog to draw and analyze a graph.",
        ),
        Token(
            {"aop", "auto"}, cli.auto_optimum_plays,
            "Runs automatically the optimum plays."
        ),
        Token(
            {"h", "-h", "help", "--help", "/?", "/h", "-?"}, print_help,
            "Prints this help message.",
        ),
    ])

    if len(arguments) < 2:
        print(f"(!) Not enough arguments (args:{arguments}).\n")
        print_help()
        return

    parser.parse(arguments)

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
