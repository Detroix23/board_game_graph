"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/tests.py
"""
import pprint

import numpy

from utilities.debug import assert_eq
from tic_tac_toe_detroix23.definitions import Board, Graph, LayoutEngine
from tic_tac_toe_detroix23 import (
    configurations, plays, conditions, ui, graphs, exports, graphing 
)


def configurations1() -> None:
	print("\n## Test: configurations 1.")

	size: tuple[int, int] = (3, 3)
	player_count: int = 2

	b1: Board = configurations.empty(size)
	c1: configurations.Configuration = configurations.Configuration(
		size,
		player_count,
		b1,
	)
	assert_eq(c1.to_int(), 0)

	b2: Board = numpy.array([
		0, 2, 1,
		0, 1, 2,
		0, 2, 1,
	])
	c2: configurations.Configuration = configurations.Configuration(
		size,
		player_count,
		b2,
	)

	b3: Board = numpy.array([
		2, 2, 2,
		2, 2, 2,
		2, 2, 2,
	])
	print(f"Image_max: {configurations.image(b3, player_count + 1)}")

	assert_eq(c2.to_int(), 5245)
	assert_eq(c2.get(0, 0), 0)
	assert_eq(c2.get(1, 0), 2)
	assert_eq(c2.get(2, 0), 1)
	assert_eq(c2.get(0, 1), 0)
	assert_eq(c2.get(1, 1), 1)
	assert_eq(c2.get(2, 1), 2)
	assert_eq(c2.get(0, 2), 0)
	assert_eq(c2.get(1, 2), 2)
	assert_eq(c2.get(2, 2), 1)

	assert_eq(b1, configurations.reverse_image(
		configurations.image(b1, player_count + 1),
		player_count + 1,
		len(b1),
	))

	assert_eq(b2, configurations.reverse_image(
		configurations.image(b2, player_count + 1),
		player_count + 1,
		len(b2),
	))

	print("\n(?) Test passed: configurations 1.")

	return

def next_configuration1() -> None:
    print("\n## Test: next_configurations 1.")
    size: tuple[int, int] = (3, 3)
    player_count: int = 2

    b1: Board = configurations.empty((3, 3))
    assert_eq(configurations.image(b1, player_count + 1), 0)
    
    b1_next = plays.next_board(b1, size,1,)
    assert b1_next is not None
    for index, board in enumerate(b1_next):
        assert_eq(configurations.image(board, player_count + 1), 3 ** (len(b1_next) - index - 1))    


    b2: Board = numpy.array([
        0, 2, 1,
        0, 1, 2,
        0, 2, 1,
    ])
    print("b2", b2)
    print("next", plays.next_board(
        b2,
        (3, 3),
        1,
    ))

    print("\n(?) Test passed: next_configurations 1.")
    return

def generate_board_graph1() -> None:
    """
    Depth = -1.
    """
    print("\n## Test: generate_board_graph 1.")

    size: tuple[int, int] = (3, 3)
    win_length: int = 3
    player_count: int = 2
    player_start: int = 2
    board_start = configurations.empty(size)
    node_start: int = configurations.image(board_start, player_count + 1)

    win_conditions = conditions.WinConditions(
        size,
        player_count,
        win_length,
    )
    win_conditions.generate()

    graph: Graph = plays.generate_graph(
        board_start,
        size,
        player_start,
        player_count,
        win_conditions,
        depth=-1,
    )

    # Data analysis.
    print(f"Graph node count: q={len(graph)}")

    graph_index = graphs.indexing(
        graph,
        node_start,
        player_start,
        player_count,
        win_conditions,
        depth_start=0,
    )

    ## Collecting end states:
    end_states: dict[int, int] = {
        -1: 0,
        0: 0,
        1: 0,
        2: 0,
    }
    for node_state in graph_index:
        end_states[node_state.win_state] += 1

    print("End states: ")
    pprint.pprint(end_states)

    # Exporting and graphing.
    exports.play_graph("ttt_graph0_3x3_d-1", graph, size, 1, player_count, 2)

    draw: bool = False
    if draw:
        graph_drawer = graphing.GraphDrawer(
            f"graph{node_start}_{size[0]}x{size[1]}_d-1",  
            graph,
            graph_index,
            configurations.image(board_start, player_count + 1),
            player_start,
            player_count,
            win_conditions,
        )
        graph_drawer.draw()
    
    return

def generate_board_graph2() -> None:
    """
    Depth = 3.
    """
    print("\n## Test: generate_board_graph 2.")

    size: tuple[int, int] = (3, 3)
    win_length: int = 3
    player_count: int = 2
    player_start: int = 1
    depth: int = 3
    board_start = numpy.array([
        0, 0, 0,
        0, 2, 0,
        0, 1, 1,
    ])
    node_start: int = configurations.image(board_start, player_count + 1)

    win_conditions = conditions.WinConditions(
        size,
        player_count,
        win_length,
    )
    win_conditions.generate()

    graph: Graph = plays.generate_graph(
        #configurations.empty(size),
        board_start,
        size,
        player_start,
        player_count,
        win_conditions,
        depth=depth,
    )

    print(f"Graph dictionary: \n{ui.format_graph(graph)}", end="\n\n")

    # Data analysis.
    graph_index = graphs.indexing(
        graph,
        node_start,
        player_start,
        player_count,
        win_conditions,
        depth_start=0,
    )

    # Exporting and drawing.
    #exports.export_play_graph("ttt_0_3x3_d2", graph1, size, 1, player_count, 2)

    graph_drawer = graphing.GraphDrawer(
        f"graph{node_start}_{size[0]}x{size[1]}_d{depth}", 
        graph,
        graph_index,
        configurations.image(board_start, player_count + 1),
        player_start,
        player_count,
        win_conditions,
        layout_engine=LayoutEngine.NEATO,
    )
    graph_drawer.draw()

    return

def win_conditions1() -> None:
	size: tuple[int, int] = (3, 3)
	player_count: int = 2

	win_generator = conditions.WinConditions(
		size,
		player_count,
		win_length=3
	)

	win_configurations: set[int] = win_generator.generate()

	print(f"win_configurations (l={len(win_configurations)}): {win_configurations}")
	
	exports.win_images(
		"ttt_wins_p2_3x3",
		win_configurations,
		size,
		player_count,
	)

	return
