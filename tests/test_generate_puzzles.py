import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from puzzle import Puzzle


def test_generate_puzzles():
    sizes = [(3, 3), (1, 5), (5, 2), (10, 10)]

    for size in sizes:
        print(f"Génère puzzle de taille {size}:")
        puzzle = Puzzle(size)
        puzzle.generate()
        print(puzzle)
        print()


if __name__ == "__main__":
    test_generate_puzzles()
