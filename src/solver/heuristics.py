from typing import Dict, List

Grid = List[List[List[int]]]


def count_mismatches(grid: Grid) -> int:
    """Heuristique basique: compte le nombre de connexions invalides."""
    height, width = len(grid), len(grid[0])
    mismatches = 0

    for y in range(height):
        for x in range(width):
            if x < width - 1 and grid[y][x][1] != grid[y][x + 1][3]:
                mismatches += 1
            if y < height - 1 and grid[y][x][2] != grid[y + 1][x][0]:
                mismatches += 1

    return mismatches


def advanced_heuristic(grid: Grid) -> int:
    """Heuristique avancée: considère aussi les bords et coûts de rotation."""
    height, width = len(grid), len(grid[0])
    score = count_mismatches(grid)

    # Pénalités bords
    for x in range(width):
        if x != 0 and grid[0][x][0] != 0:
            score += 2
        if x != width - 1 and grid[height - 1][x][2] != 0:
            score += 2

    for y in range(height):
        if y != 0 and grid[y][0][3] != 0:
            score += 2
        if y != height - 1 and grid[y][width - 1][1] != 0:
            score += 2

    return score
