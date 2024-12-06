from src.grid.grid import generate_puzzle
from src.solver.terminal_checker import is_terminal_state


def test_is_terminal():
    grid = generate_puzzle(5, 5)
    print("État initial:", is_terminal_state(grid))


def test_known_terminal():
    known_solved = [[[1, 0, 1, 0], [0, 1, 0, 1]], [[0, 1, 0, 1], [1, 0, 1, 0]]]
    print("État connu résolu:", is_terminal_state(known_solved))


if __name__ == "__main__":
    test_is_terminal()
    test_known_terminal()
