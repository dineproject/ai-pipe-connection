from typing import List, Tuple

from core.models.tile import Tile, TileType


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

    def set_tile(self, tile: Tile, position: Tuple[int, int]) -> None:
        """
        Définit une tuile à une position donnée sur le plateau.

        Args:
            tile: La tuile à placer
            position: La position de la tuile sous forme de tuple (ligne, colonne)

        Raises:
            ValueError: Si la position est en dehors du plateau
        """
        if not self.is_valid_position(position):
            raise ValueError("Position en dehors du plateau")
        self.tiles[position[0]][position[1]] = tile

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        """
        Retourne la tuile à une position donnée sur le plateau.

        Args:
            position: La position de la tuile sous forme de tuple (ligne, colonne)

        Returns:
            Tile: La tuile à la position donnée

        Raises:
            ValueError: Si la position est en dehors du plateau
        """
        if not self.is_valid_position(position):
            raise ValueError("Position en dehors du plateau")
        return self.tiles[position[0]][position[1]]

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Vérifie si une position est valide sur le plateau.

        Args:
            position: La position à vérifier

        Returns:
            bool: True si la position est valide, False sinon
        """
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Retourne les positions des voisins, tuiles adjacentes, d'une position donnée.

        Args:
            position: La position dont on veut les voisins

        Returns:
            List[Tuple[int, int]]: La liste des positions des voisins
        """
        neighbors = []
        if position[0] > 0:
            neighbors.append((position[0] - 1, position[1]))
        if position[0] < self.height - 1:
            neighbors.append((position[0] + 1, position[1]))
        if position[1] > 0:
            neighbors.append((position[0], position[1] - 1))
        if position[1] < self.width - 1:
            neighbors.append((position[0], position[1] + 1))
        return neighbors

    def are_tiles_neighbors(
        self, position1: Tuple[int, int], position2: Tuple[int, int]
    ) -> bool:
        """
        Vérifie si deux positions de tuiles sont voisines.

        Args:
            position1: La première position
            position2: La deuxième position

        Returns:
            bool: True si les positions sont voisines, False sinon
        """
        return position2 in self.get_neighbors(position1)

    def is_safe_pair(
        self, position1: Tuple[int, int], position2: Tuple[int, int]
    ) -> bool:
        """
        Vérifie si deux tuiles sont compatibles l'une avec l'autre.

        Args:
            position1: La position de la première
            position2: La position de la deuxième

        Returns:
            bool: True si les tuiles sont compatibles, False sinon
        """

        pass

    def __str__(self) -> str:
        board_str = "Plateau de jeu:\n"
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.get_tile((x, y))
                if tile.type == TileType.EMPTY:
                    row.append(".")
                else:
                    row.append(str(tile))
            board_str += " ".join(row) + "\n"
        return board_str

    def is_valid_connection(
        self, pos1: Tuple[int, int], pos2: Tuple[int, int]
    ) -> bool:
        """
        Vérifie si deux tuiles adjacentes forment une connexion valide
        (ouvert-ouvert ou fermé-fermé)

        Args:
            pos1: La position de la première tuile
            pos2: La position de la deuxième tuile

        Returns:
            bool: True si la connexion est valide, False sinon
        """
        if not self.are_neighbors(pos1, pos2):
            return False

        tile1 = self.get_tile(pos1)
        tile2 = self.get_tile(pos2)

        x1, y1 = pos1
        x2, y2 = pos2

        # Déterminer le côté à vérifier
        if x2 > x1:
            dir1, dir2 = Direction.RIGHT, Direction.LEFT
        elif x2 < x1:
            dir1, dir2 = Direction.LEFT, Direction.RIGHT
        elif y2 > y1:
            dir1, dir2 = Direction.DOWN, Direction.UP
        else:
            dir1, dir2 = Direction.UP, Direction.DOWN

        openings1 = tile1.get_openings()
        openings2 = tile2.get_openings()

        # Les deux côtés doivent être soit ouverts, soit fermés
        return openings1[dir1] == openings2[dir2]
