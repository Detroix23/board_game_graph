"""
# Board game graphing: Tic-Tac-Toe.
/src/tic_tac_toe_detroix23/__main__.py
"""
import numpy

from utilities.debug import assert_eq
from tic_tac_toe_detroix23.configurations import Configuration

def main() -> None:
	"""
	Main entry point for `tic_tac_toe_detroix23`.
	"""
	print("\n# Board game graphing.\n")

	test_configurations1()

	return

def test_configurations1() -> None:
	print("\n## Test: configurations 1.")

	c1: Configuration = Configuration.new_empty((3, 3), 2)
	assert_eq(c1.to_int(), 0)

	c2: Configuration = Configuration(
		(3, 3),
		2,
		numpy.array([
			0, 2, 1,
			0, 1, 2,
			0, 2, 1,
		])
	)
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

	print("\n(?) Test passed: configurations 1.")
	return

main()
