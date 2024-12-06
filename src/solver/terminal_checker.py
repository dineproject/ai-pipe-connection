from typing import List

Grid = List[List[List[int]]]


def is_terminal_state(grid: Grid) -> bool:
    """Vérifie si l'état est terminal (puzzle résolu)."""
    height, width = len(grid), len(grid[0])

    # Vérification des connexions internes
    for y in range(height):
        for x in range(width):
            if x < width - 1 and grid[y][x][1] != grid[y][x + 1][3]:
                return False
            if y < height - 1 and grid[y][x][2] != grid[y + 1][x][0]:
                return False

    # Vérification des bords
    for x in range(width):
        if x != 0 and grid[0][x][0] != 0:
            return False
        if x != width - 1 and grid[height - 1][x][2] != 0:
            return False

    for y in range(height):
        if y != 0 and grid[y][0][3] != 0:
            return False
        if y != height - 1 and grid[y][width - 1][1] != 0:
            return False

    return True
