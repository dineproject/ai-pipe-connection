import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from core.models.tile import Direction, Tile, TileType


def test_tile_properties():
    """
    Teste les propriétés et méthodes de la classe Tile.
    Tests :
    - Création de différents types de tuiles
    - Lecture des ouvertures
    - Rotations et leur impact sur les ouvertures
    """
    # Création des tuiles
    corner = Tile(TileType.CORNER)
    line = Tile(TileType.LINE)
    t_shape = Tile(TileType.T_SHAPE)

    # Test création
    print("=== Test création de tuiles ===")
    print(f"CORNER: {corner}")
    print(f"LINE: {line}")
    print(f"T_SHAPE: {t_shape}")

    # Test des ouvertures d'un CORNER
    print("\n=== Test ouvertures initiales d'un CORNER ===")
    print("Ouvertures:", corner.get_openings())

    # Test des rotations et leur impact
    print("\n=== Test rotations d'un CORNER ===")

    corner.rotate()  # Rotation de 90°
    print("Après rotation 90°:")
    print(f"- État: {corner}")
    print(f"- Ouvertures: {corner.get_openings()}")

    corner.rotate(2)  # Deux rotations supplémentaires = +180°
    print("\nAprès 2 rotations supplémentaires (270° total):")
    print(f"- État: {corner}")
    print(f"- Ouvertures: {corner.get_openings()}")


if __name__ == "__main__":
    test_tile_properties()
