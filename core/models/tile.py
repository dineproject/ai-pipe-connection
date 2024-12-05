from enum import Enum
from typing import Dict


class Direction(Enum):
    UP = "haut"
    DOWN = "bas"
    LEFT = "gauche"
    RIGHT = "droite"


class TileType(Enum):
    EMPTY = "vide"
    CROSS = "croix"  # ┼
    T_SHAPE = "t"  # ┬
    LINE = "ligne"  # ─
    CORNER = "angle"  # ┐
    HALF = "demi"  # une demi-tuile


class Tile:
    """
    Représente une tuile du jeu avec un type spécifique et une rotation.
    Une tuile possède des ouvertures dans différentes directions qui peuvent être connectées à d'autres tuiles.
    """

    def __init__(self, tile_type: TileType, rotation: int = 0):
        """
        Initialise une nouvelle tuile.

        Args:
            tile_type: Le type de la tuile
            rotation: La rotation de la tuile en degrés (0, 90, 180 ou 270)

        Raises:
            ValueError: Si la rotation n'est pas un multiple de 90
        """
        if rotation % 90 != 0:
            raise ValueError("La rotation doit être un multiple de 90 degrés")

        self.type = tile_type
        self.rotation = rotation
        self.openings = self._get_base_openings()

    def _get_base_openings(self) -> Dict[Direction, int]:
        """
        Retourne la configuration de base des ouvertures selon le type de tuile.

        Returns:
            Dict[Direction, int]: Dictionnaire avec les directions comme clés
            et 1 (ouvert) ou 0 (fermé) comme valeurs
        """
        base_openings = {
            TileType.EMPTY: {d: 0 for d in Direction},
            TileType.CROSS: {d: 1 for d in Direction},
            TileType.T_SHAPE: {
                Direction.UP: 1,
                Direction.RIGHT: 1,
                Direction.DOWN: 1,
                Direction.LEFT: 0,
            },
            TileType.LINE: {
                Direction.UP: 0,
                Direction.RIGHT: 1,
                Direction.DOWN: 0,
                Direction.LEFT: 1,
            },
            TileType.CORNER: {
                Direction.UP: 0,
                Direction.RIGHT: 0,
                Direction.DOWN: 1,
                Direction.LEFT: 1,
            },
            TileType.HALF: {
                Direction.UP: 0,
                Direction.RIGHT: 0,
                Direction.DOWN: 0,
                Direction.LEFT: 1,
            },
        }
        return base_openings[self.type]

    def rotate(self, times: int = 1) -> None:
        """
        Effectue une ou plusieurs rotations horaires de 90 degrés de la tuile.

        Args:
            times: Nombre de rotations de 90° à effectuer (par défaut 1)
        """
        self.rotation = (self.rotation + 90 * times) % 360

    def get_openings(self) -> Dict[Direction, int]:
        """
        Retourne les ouvertures de la tuile en tenant compte de sa rotation.

        Returns:
            Dict[Direction, int]: Dictionnaire avec les directions comme clés
            et 1 (ouvert) ou 0 (fermé) comme valeurs
        """
        if self.rotation == 0:
            return self.openings

        # Calcul des nouvelles directions après rotation
        rotated_openings = {}
        for direction in Direction:
            # Trouver la direction d'origine avant rotation
            if self.rotation == 90:
                if direction == Direction.UP:
                    orig = Direction.LEFT
                elif direction == Direction.RIGHT:
                    orig = Direction.UP
                elif direction == Direction.DOWN:
                    orig = Direction.RIGHT
                else:
                    orig = Direction.DOWN
            elif self.rotation == 180:
                if direction == Direction.UP:
                    orig = Direction.DOWN
                elif direction == Direction.RIGHT:
                    orig = Direction.LEFT
                elif direction == Direction.DOWN:
                    orig = Direction.UP
                else:
                    orig = Direction.RIGHT
            else:
                if direction == Direction.UP:
                    orig = Direction.RIGHT
                elif direction == Direction.RIGHT:
                    orig = Direction.DOWN
                elif direction == Direction.DOWN:
                    orig = Direction.LEFT
                else:
                    orig = Direction.UP

            rotated_openings[direction] = self.openings[orig]

        return rotated_openings

    def __str__(self) -> str:
        return f"Tile({self.type}, rotation={self.rotation})"
