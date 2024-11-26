class Tile:
    """
    Représente une tuile individuelle du puzzle.
    Attributes:
        north: L'état du côté nord de la tuile (0 pour fermé, 1 pour ouvert).
        east: L'état du côté est de la tuile.
        south: L'état du côté sud de la tuile.
        west: L'état du côté ouest de la tuile.
    """

    def __init__(self, north: int, east: int, south: int, west: int):
        """
        Initialise une nouvelle instance de la classe Tile.
        Args:
            north: L'état initial du côté nord de la tuile.
            east: L'état initial du côté est de la tuile.
            south: L'état initial du côté sud de la tuile.
            west: L'état initial du côté ouest de la tuile.
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def __str__(self) -> str:
        return f"({self.north}, {self.east}, {self.south}, {self.west})"

    def rotate(self) -> None:
        """
        Fait pivoter la tuile de 90 degrés dans le sens horaire.
        """
        self.north, self.east, self.south, self.west = (
            self.west,
            self.north,
            self.east,
            self.south,
        )

    def is_compatible(self, other: "Tile", direction: str) -> bool:
        """
        Vérifie si la tuile est compatible avec une autre tuile dans une direction donnée.

        Args:
            other: L'autre tuile à comparer.
            direction: La direction dans laquelle vérifier la compatibilité.
                Doit être une des valeurs suivantes : "north", "east", "south", "west".

        Returns:
            True si les tuiles sont compatibles dans la direction donnée, False sinon.
        """
        if direction == "north":
            return self.north == other.south
        elif direction == "east":
            return self.east == other.west
        elif direction == "south":
            return self.south == other.north
        elif direction == "west":
            return self.west == other.east
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def get_neighbor(self, direction: str) -> int:
        """
        Renvoie l'état du côté voisin dans une direction donnée.

        Args:
            direction: La direction du voisin ('north', 'east', 'south', 'west').

        Returns:
            L'état du côté voisin (0 ou 1).
        """
        if direction == "north":
            return self.north
        elif direction == "east":
            return self.east
        elif direction == "south":
            return self.south
        elif direction == "west":
            return self.west
        else:
            raise ValueError(f"Invalid direction: {direction}")
