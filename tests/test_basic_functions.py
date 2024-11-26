import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.puzzle import TILE_CORNER, TILE_LINE, TILE_T, Puzzle


def test_basic_functions():
    # Créer un nouveau puzzle de taille 3x3
    puzzle = Puzzle((3, 3))

    # Afficher le puzzle initial (vide)
    print("Puzzle initial :")
    print(puzzle)

    # Placer quelques tuiles
    puzzle.set_tile((0, 0), TILE_CORNER)
    puzzle.set_tile((1, 1), TILE_T)
    puzzle.set_tile((2, 2), TILE_LINE)

    # Afficher le puzzle avec les tuiles placées
    print("\nPuzzle avec des tuiles placées :")
    print(puzzle)

    # Faire pivoter une tuile
    puzzle.rotate_tile((1, 1))

    # Afficher le puzzle après la rotation
    print("\nPuzzle après la rotation d'une tuile :")
    print(puzzle)


if __name__ == "__main__":
    test_basic_functions()
