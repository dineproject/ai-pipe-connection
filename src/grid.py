import random
from typing import List, Tuple

Grid = List[List[List[int]]]
Position = Tuple[int, int]


def create_empty_grid(width: int, height: int) -> Grid:
    """Crée une grille vide de dimensions données"""
    return [[[0, 0, 0, 0] for _ in range(width)] for _ in range(height)]


def generate_path(width: int, height: int) -> List[Position]:
    """
    Génère un chemin valide de (0,0) à (width-1,height-1).
    Le chemin ne peut aller que droite/bas/gauche.
    La direction opposée au dernier mouvement est interdite.
    """
    path = [(0, 0)]
    x, y = 0, 0
    last_dir = None

    while (x, y) != (width - 1, height - 1):
        moves = []
        if x < width - 1 and last_dir != "left":
            moves.append((x + 1, y, "right"))
        if y < height - 1:
            moves.append((x, y + 1, "down"))
        if x > 0 and y < height - 1 and last_dir != "right":
            moves.append((x - 1, y, "left"))

        if not moves:
            return generate_path(width, height)

        x, y, last_dir = random.choice(moves)
        path.append((x, y))

    return path


def set_initial_tiles(grid: Grid, path: List[Position]) -> None:
    """
    Place des tuiles LINE ou CORNER le long du chemin.
    - Première tuile: LINE si vers (1,0), sinon CORNER
    - Dernière tuile: LINE si dernière ligne, sinon CORNER
    - Tuiles intermédiaires: LINE si même direction, CORNER si changement
    """
    for i, pos in enumerate(path):
        if i == 0:
            next_pos = path[i + 1]
            tile = [0, 1, 0, 1] if next_pos[0] == 1 else [0, 1, 1, 0]

        elif i == len(path) - 1:
            prev = path[i - 1]
            tile = [0, 1, 0, 1] if prev[1] == len(grid) - 1 else [1, 1, 0, 0]

        else:
            prev, next_pos = path[i - 1], path[i + 1]
            dx1, dy1 = pos[0] - prev[0], pos[1] - prev[1]
            dx2, dy2 = next_pos[0] - pos[0], next_pos[1] - pos[1]
            tile = (
                [0, 1, 0, 1]
                if (dx1, dy1) == (dx2, dy2) and dx1 != 0
                else [1, 0, 1, 0] if (dx1, dy1) == (dx2, dy2) else [1, 1, 0, 0]
            )

        grid[pos[1]][pos[0]] = tile


def count_empty_neighbors(grid: Grid, pos: Position) -> List[Position]:
    """Trouve les positions des voisins vides d'une case donnée"""
    x, y = pos
    empty = []
    for nx, ny in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
        if (
            0 <= nx < len(grid[0])
            and 0 <= ny < len(grid)
            and grid[ny][nx] == [0, 0, 0, 0]
        ):
            empty.append((nx, ny))
    return empty


def add_connections(grid: Grid, path: List[Position]) -> None:
    """
    Complexifie le chemin selon les voisins vides:
    - 1 voisin vide: T_SHAPE + HALF
    - 2 voisins vides: CROSS + 2 HALF
    """
    for pos in path:
        empty = count_empty_neighbors(grid, pos)

        if len(empty) == 1:
            grid[pos[1]][pos[0]] = [1, 1, 1, 0]
            grid[empty[0][1]][empty[0][0]] = [0, 0, 0, 1]

        elif len(empty) == 2:
            grid[pos[1]][pos[0]] = [1, 1, 1, 1]
            for ex, ey in empty:
                grid[ey][ex] = [0, 0, 0, 1]


def rotate_randomly(grid: Grid) -> None:
    """Applique des rotations aléatoires aux tuiles (sauf EMPTY et CROSS)"""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != [0, 0, 0, 0] and grid[y][x] != [1, 1, 1, 1]:
                rotations = random.randint(0, 3)
                grid[y][x] = grid[y][x][-rotations:] + grid[y][x][:-rotations]


def generate_puzzle(width: int, height: int) -> Grid:
    """
    Génère un puzzle valide selon l'approche:
    1. Génération d'un chemin valide
    2. Placement des tuiles initiales
    3. Complexification avec T_SHAPE/CROSS
    4. Rotations aléatoires
    """
    grid = create_empty_grid(width, height)
    path = generate_path(width, height)
    set_initial_tiles(grid, path)
    add_connections(grid, path)
    rotate_randomly(grid)
    return grid
