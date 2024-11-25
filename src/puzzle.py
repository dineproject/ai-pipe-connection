from tile import Tile
from typing import Tuple, List

TILE_EMPTY = Tile(0, 0, 0, 0)
TILE_CORNER = Tile(0, 1, 1, 0)
TILE_LINE = Tile(1, 0, 1, 0)
TILE_T = Tile(1, 1, 1, 0)
TILE_CROSS = Tile(1, 1, 1, 1)

class Puzzle:
    """
    Représente un puzzle entier composé d'une grille de tuiles.
    Attributes:
        size: Les dimensions (lignes, colonnes) de la grille du puzzle.
        grid: La grille du puzzle, représentée par une liste de listes de tuiles.
    """
    def __init__(self, size: Tuple[int, int]):
        """
        Initialise une nouvelle instance de la classe Puzzle.
        Args:
            size: Les dimensions (lignes, colonnes) de la grille du puzzle.
        """
        self.size: Tuple[int, int] = size
        self.grid: List[List[Tile]] = [[TILE_EMPTY] * size[1] for _ in range(size[0])]

    def __str__(self) -> str:
        return "\n".join(" ".join(str(tile) for tile in row) for row in self.grid)

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Vérifie si la position donnée est valide dans la grille du puzzle.
        Args:
            position: Un tuple (ligne, colonne) représentant la position à vérifier.
        Returns:
            True si la position est valide, False sinon.
        """
        row, col = position
        return 0 <= row < self.size[0] and 0 <= col < self.size[1]

    def set_tile(self, position: Tuple[int, int], tile: Tile) -> None:
        """
        Place une tuile à une position donnée dans la grille du puzzle.
        Args:
            position: Un tuple (ligne, colonne) représentant la position où placer la tuile.
            tile: La tuile à placer.
        """
        if self.is_valid_position(position):
            row, col = position
            self.grid[row][col] = tile

    def rotate_tile(self, position: Tuple[int, int]) -> None:
        """
        Fait pivoter la tuile à une position donnée dans la grille du puzzle.
        Args:
            position: Un tuple (ligne, colonne) représentant la position de la tuile à faire pivoter.
        """
        if self.is_valid_position(position):
            row, col = position
            self.grid[row][col].rotate()