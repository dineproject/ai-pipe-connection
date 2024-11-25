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
        self.north, self.east, self.south, self.west = self.west, self.north, self.east, self.south