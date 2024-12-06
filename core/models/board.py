from typing import List, Tuple

from core.models.tile import Direction, Tile, TileType


class Board:
    """
    Classe représentant le plateau de jeu.
    """

    def __init__(self, width: int, height: int):
        """
        Initialise un nouveau plateau de jeu.

        Args:
            width: La largeur du plateau
            height: La hauteur du plateau
        """
        self.width = width
        self.height = height
        self.tiles = [
            [Tile(TileType.EMPTY) for _ in range(width)] for _ in range(height)
        ]

    def __str__(self) -> str:
        tile_symbols = {
            TileType.EMPTY: ".",
            TileType.CORNER: ["┏", "┓", "┛", "┗"],
            TileType.LINE: ["━", "┃"],
            TileType.T_SHAPE: ["┳", "┣", "┻", "┫"],
            TileType.CROSS: "┼",
            TileType.HALF: ["↓", "→", "↑", "←"],
        }

        board_repr = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.tiles[y][x]
                if isinstance(tile_symbols[tile.type], str):
                    # Si c'est une chaîne simple (EMPTY ou CROSS)
                    row.append(tile_symbols[tile.type])
                else:
                    # Si c'est une liste de symboles
                    index = (tile.rotation // 90) % len(tile_symbols[tile.type])
                    row.append(tile_symbols[tile.type][index])
            board_repr.append(" ".join(row))
        return "\n".join(board_repr)

    def set_tile(self, tile: Tile, position: Tuple[int, int]) -> None:
        """
        Définit une tuile à une position donnée sur le plateau.

        Args:
            tile: La tuile à placer
            position: La position de la tuile sous forme de tuple (ligne, colonne)
        """
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile
        else:
            raise ValueError("Position en dehors du plateau")

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        """
        Retourne la tuile à une position donnée sur le plateau.

        Args:
            position: La position de la tuile sous forme de tuple (ligne, colonne)
        """
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        else:
            raise ValueError("Position en dehors du plateau")

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Retourne les positions des voisins, tuiles adjacentes, d'une position donnée.

        Args:
            position: La position dont on veut les voisins
        """
        neighbors = []
        x, y = position

        if x > 0:
            neighbors.append((x - 1, y))  # Voisin de gauche
        if x < self.width - 1:
            neighbors.append((x + 1, y))  # Voisin de droite
        if y > 0:
            neighbors.append((x, y - 1))  # Voisin du haut
        if y < self.height - 1:
            neighbors.append((x, y + 1))  # Voisin du bas

        return neighbors

    def are_neighbors(
        self, position1: Tuple[int, int], position2: Tuple[int, int]
    ) -> bool:
        """
        Vérifie si deux positions de tuiles sont voisines, adjacentes (en ligne ou en colonne).
        """
        x1, y1 = position1
        x2, y2 = position2

        return (abs(x1 - x2) == 1 and y1 == y2) or (
            abs(y1 - y2) == 1 and x1 == x2
        )
