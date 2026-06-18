"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/__main__.py
"""
import numpy

from utilities.debug import assert_eq
from tic_tac_toe_detroix23.definitions import Board, Graph
from tic_tac_toe_detroix23 import configurations, plays, ui, exports

def test_configurations1() -> None:
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

def test_next_configuration1() -> None:
	print("\n## Test: next_configurations 1.")

	b1: Board = configurations.empty((3, 3))
	print(b1)
	print(plays.next_board(
		b1,
		(3, 3),
		1,
	))

	b2: Board = numpy.array([
		0, 2, 1,
		0, 1, 2,
		0, 2, 1,
	])
	print(b2)
	print(plays.next_board(
		b2,
		(3, 3),
		1,
	))

	return

def test_generate_board_graph1() -> None:
	print("\n## Test: generate_board_graph 1.")

	size: tuple[int, int] = (3, 3)
	player_count: int = 2
	graph1: Graph = plays.generate_plays_graph(
		configurations.empty(size),
		size,
		1,
		player_count,
		2,
	)

	print(ui.format_graph(graph1), end="\n\n")

	print(ui.format_board(configurations.reverse_image(0, player_count + 1, size[0] * size[1]), size))
	print(ui.format_board(configurations.reverse_image(1, player_count + 1, size[0] * size[1]), size))
	print(ui.format_board(configurations.reverse_image(6561, player_count + 1, size[0] * size[1]), size))
	print(ui.format_board(configurations.reverse_image(13123, player_count + 1, size[0] * size[1]), size))

	exports.export_play_graph("graph0_3x3_d2", graph1, size, 1, player_count, 2)
	
	return

def test_generate_board_graph2() -> None:
	print("\n## Test: generate_board_graph 2.")

	size: tuple[int, int] = (3, 3)
	player_count: int = 2
	graph1: Graph = plays.generate_plays_graph(
		configurations.empty(size),
		size,
		1,
		player_count,
	)

	print(len(graph1))
	exports.export_play_graph("graph0_3x3", graph1, size, 1, player_count, 2)

	return

def main() -> None:
	"""
	Main entry point for `tic_tac_toe_detroix23`.
	"""
	print("\n# Board game graphing.\n")

	test_configurations1()

	test_next_configuration1()

	test_generate_board_graph1()

	test_generate_board_graph2()

	return

main()
