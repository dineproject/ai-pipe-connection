import random
from typing import List, Tuple

from tile import Tile

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

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Renvoie les positions valides des voisins d'une position donnée.

        Args:
            position: La position dont on veut obtenir les voisins.

        Returns:
            Une liste des positions valides des voisins.
        """
        row, col = position
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position((new_row, new_col)):
                neighbors.append((new_row, new_col))
        return neighbors

    def is_path_valid(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """
        Vérifie s'il existe un chemin valide entre une position de départ et une position finale.

        Args:
            start: La position de départ.
            end: La position finale.

        Returns:
            True s'il existe un chemin valide, False sinon.
        """
        if start == end:
            return True
        for neighbor in self.get_neighbors(start):
            if self.grid[neighbor[0]][neighbor[1]] == TILE_EMPTY:
                for tile_type in [TILE_CORNER, TILE_LINE, TILE_T, TILE_CROSS]:
                    tile = tile_type
                    if self.is_tile_compatible(tile, neighbor):
                        self.set_tile(neighbor, tile)
                        if self.is_path_valid(neighbor, end):
                            return True
                        self.set_tile(neighbor, TILE_EMPTY)
        return False

    def is_tile_compatible(self, tile: Tile, position: Tuple[int, int]) -> bool:
        """
        Vérifie si une tuile est compatible avec les tuiles voisines à une position donnée.

        Args:
            tile: La tuile à vérifier.
            position: La position où placer la tuile.

        Returns:
            True si la tuile est compatible, False sinon.
        """
        for neighbor, direction in zip(
            self.get_neighbors(position), ["north", "east", "south", "west"]
        ):
            if not self.is_valid_position(neighbor):
                continue
            neighbor_tile = self.grid[neighbor[0]][neighbor[1]]
            if neighbor_tile != TILE_EMPTY and not tile.is_compatible(
                neighbor_tile, direction
            ):
                return False
        return True

    def fill_grid(self) -> None:
        """
        Remplit les positions vides de la grille avec des tuiles aléatoires compatibles.
        """
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.grid[row][col] == TILE_EMPTY:
                    compatible_tiles = [
                        tile
                        for tile in [TILE_CORNER, TILE_LINE, TILE_T, TILE_CROSS]
                        if self.is_tile_compatible(tile, (row, col))
                    ]
                    if compatible_tiles:
                        self.set_tile((row, col), random.choice(compatible_tiles))

    def shuffle_grid(self) -> None:
        """
        Applique des rotations aléatoires à certaines tuiles de la grille.
        """
        for _ in range(self.size[0] * self.size[1] // 2):
            row, col = random.randint(0, self.size[0] - 1), random.randint(
                0, self.size[1] - 1
            )
            self.rotate_tile((row, col))

    def generate(self) -> None:
        """
        Génère un nouveau puzzle solvable.
        """
        start, end = (0, 0), (self.size[0] - 1, self.size[1] - 1)
        self.set_tile(start, TILE_CORNER)
        self.set_tile(end, TILE_CORNER)
        self.is_path_valid(start, end)
        self.fill_grid()
        self.shuffle_grid()
