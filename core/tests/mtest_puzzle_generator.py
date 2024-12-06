import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from core.generators.puzzle_generator import *
from core.models.board import Board
from core.models.tile import Tile, TileType


def test_generate_path():
    """Test la génération du chemin"""
    board = Board(5, 5)
    path = generate_path(board)
    print("\n=== Test génération du chemin ===")
    print("Chemin généré:", path)


def test_place_initial_tuiles():
    """Test le placement initial des tuiles"""
    board = Board(5, 6)
    path = generate_path(board)
    set_initial_tuiles(board, path)
    print("\n=== Test placement initial des tuiles ===")
    print("Chemin:", path)
    print("\nPlateau:")
    print(board)


def test_add_complex_tuiles_and_fill_spaces():
    """Test le processus complet de génération"""
    board = Board(5, 5)
    path = generate_path(board)

    print("\n=== Test génération complète ===")
    print("Chemin généré:", path)

    print("\n1. Après placement initial:")
    set_initial_tuiles(board, path)
    print(board)

    print("\n2. Après ajout des connexions:")
    add_connections(board, path)
    print(board)

    print("\n3. Après remplissage des espaces:")
    fill_empty_spaces(board)
    print(board)

    print("\n4. Après rotations aléatoires:")
    randomize_rotations(board)
    print(board)


def test_generate_puzzle():
    """Test la fonction de génération complète"""
    print("\n=== Test generate_puzzle ===")
    board = generate_puzzle(500, 500)
    print(board)


if __name__ == "__main__":
    # test_generate_path()
    # test_place_initial_tuiles()
    test_add_complex_tuiles_and_fill_spaces()
    # test_generate_puzzle()
