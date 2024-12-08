import copy
import heapq
from datetime import datetime
from typing import Callable, Dict, List, Optional, Set, Tuple, TypeVar

from .grid import generate_puzzle
from .visualizer import PuzzleVisualizer

State = TypeVar("State")
Description = TypeVar("Description")
Cost = TypeVar("Cost")
Transition = Tuple[Description, State, Cost]
Solution = List[Transition]


def is_final(grid: List[List[List[int]]]) -> bool:
    """Vérifie si l'état du puzzle est terminal (résolu)."""
    rows = len(grid)
    cols = len(grid[0])

    def check_border_cells(
        r: int, c: int, min_ones: int, max_ones: int
    ) -> bool:
        """Vérifie qu'une cellule de bord a un nombre valide de connexions."""
        tile = grid[r][c]
        return min_ones <= sum(tile) <= max_ones

    if not check_border_cells(0, 0, 1, 3):
        return False
    if not check_border_cells(rows - 1, cols - 1, 1, 3):
        return False
    if not check_border_cells(0, cols - 1, 0, 2):
        return False
    if not check_border_cells(rows - 1, 0, 0, 2):
        return False

    for c in range(1, cols - 1):
        if not check_border_cells(0, c, 0, 3):
            return False
        if not check_border_cells(rows - 1, c, 0, 3):
            return False

    for r in range(1, rows - 1):
        if not check_border_cells(r, 0, 0, 3):
            return False
        if not check_border_cells(r, cols - 1, 0, 3):
            return False

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            tile = grid[i][j]
            if tile[0] != grid[i - 1][j][2]:
                return False
            if tile[1] != grid[i][j + 1][3]:
                return False
            if tile[2] != grid[i + 1][j][0]:
                return False
            if tile[3] != grid[i][j - 1][1]:
                return False

    tile = grid[0][0]
    if tile[0] != 0:
        return False
    if tile[1] != grid[0][1][3]:
        return False
    if tile[2] != grid[1][0][0]:
        return False
    if tile[3] != 1:
        return False

    tile = grid[rows - 1][cols - 1]
    if tile[0] != grid[rows - 2][cols - 1][2]:
        return False
    if tile[1] != 1:
        return False
    if tile[2] != 0:
        return False
    if tile[3] != grid[rows - 1][cols - 2][1]:
        return False

    for j in range(1, cols - 1):
        tile = grid[0][j]
        if tile[0] != 0:
            return False
        if tile[1] != grid[0][j + 1][3]:
            return False
        if tile[3] != grid[0][j - 1][1]:
            return False

    for j in range(1, cols - 1):
        tile = grid[rows - 1][j]
        if tile[2] != 0:
            return False
        if tile[1] != grid[rows - 1][j + 1][3]:
            return False
        if tile[3] != grid[rows - 1][j - 1][1]:
            return False

    for i in range(1, rows - 1):
        tile = grid[i][0]
        if tile[3] != 0:
            return False
        if tile[0] != grid[i - 1][0][2]:
            return False
        if tile[2] != grid[i + 1][0][0]:
            return False

    for i in range(1, rows - 1):
        tile = grid[i][cols - 1]
        if tile[1] != 0:
            return False
        if tile[0] != grid[i - 1][cols - 1][2]:
            return False
        if tile[2] != grid[i + 1][cols - 1][0]:
            return False

    return True


def rotation_a_droite(tile: List[int]) -> List[int]:
    """Effectue une rotation de 90° vers la droite d'une tuile."""
    return [tile[-1]] + tile[:-1]


def double_rotation(tile: List[int]) -> List[int]:
    """Effectue une double rotation (180°) d'une tuile."""
    return rotation_a_droite(rotation_a_droite(tile))


def triple_rotation(tile: List[int]) -> List[int]:
    """Effectue une triple rotation (270°) d'une tuile."""
    return rotation_a_droite(double_rotation(tile))


def transformations(grid: List[List[List[int]]]) -> List[Transition]:
    """Génère tous les états successeurs possibles par rotation des tuiles."""
    successors = []
    rows, cols = len(grid), len(grid[0])

    for i in range(rows):
        for j in range(cols):
            tile = grid[i][j]
            if tile == [0, 0, 0, 0] or tile == [1, 1, 1, 1]:
                continue

            elif tile == [1, 0, 1, 0] or tile == [0, 1, 0, 1]:
                one_rotation = rotation_a_droite(tile)
                new_grid = copy.deepcopy(grid)
                new_grid[i][j] = one_rotation
                successors.append(("1 rotation", new_grid, 1))

            else:
                one_rotation = rotation_a_droite(tile)
                two_rotations = double_rotation(tile)
                three_rotations = triple_rotation(tile)

                for new_tile, description in zip(
                    [one_rotation, two_rotations, three_rotations],
                    ["1 rotation", "2 rotations", "3 rotations"],
                ):
                    new_grid = copy.deepcopy(grid)
                    new_grid[i][j] = new_tile
                    successors.append((description, new_grid, 1))
    return successors


def minimal_local_cost(tile: List[int], neighbors: Dict[str, List[int]]) -> int:
    """Calcule le coût minimal pour rendre une tuile compatible avec ses voisins."""
    best_cost = float("inf")
    current = tile[:]
    for _ in range(4):
        local_cost = 0
        if "right" in neighbors and current[1] != neighbors["right"][3]:
            local_cost += 1
        if "down" in neighbors and current[2] != neighbors["down"][0]:
            local_cost += 1
        if local_cost < best_cost:
            best_cost = local_cost
        current = [current[-1]] + current[:-1]
    return best_cost


def enhanced_heuristic(grid: List[List[List[int]]]) -> int:
    """Calcule un score heuristique guidant la recherche de solution."""
    rows = len(grid)
    cols = len(grid[0])
    mismatches = 0
    border_penalty = 0
    rotation_cost = 0

    for i in range(rows):
        for j in range(cols):
            tile = grid[i][j]
            neighbors = {}
            if j < cols - 1:
                neighbors["right"] = grid[i][j + 1]
                if tile[1] != grid[i][j + 1][3]:
                    mismatches += 1
            if i < rows - 1:
                neighbors["down"] = grid[i + 1][j]
                if tile[2] != grid[i + 1][j][0]:
                    mismatches += 1

            if i == 0 and tile[0] != 0:
                border_penalty += 2
            if i == rows - 1 and tile[2] != 0:
                border_penalty += 2
            if j == 0 and tile[3] != 0:
                border_penalty += 2
            if j == cols - 1 and tile[1] != 0:
                border_penalty += 2

            rotation_cost += minimal_local_cost(tile, neighbors)

    return mismatches + border_penalty + rotation_cost


def grid_to_tuple(grid: List[List[List[int]]]) -> Tuple:
    """Convertit une grille en tuple immuable pour utilisation comme clé."""
    return tuple(tuple(tuple(tile) for tile in row) for row in grid)


def a_star_solver(
    transformations: Callable[[State], List[Transition]],
    isFinal: Callable[[State], bool],
    state: State,
    heuristic: Callable[[State], int],
    max_depth: int = 100000,
) -> Optional[Solution]:
    """Résout le puzzle avec l'algorithme A*."""
    frontier = []
    initial_h = heuristic(state)
    heapq.heappush(frontier, (initial_h, 0, state, []))
    visited = set([grid_to_tuple(state)])

    while frontier:
        f, g, current_state, path = heapq.heappop(frontier)

        if isFinal(current_state):
            return path

        if g > max_depth:
            continue

        for description, next_state, cost in transformations(current_state):
            state_key = grid_to_tuple(next_state)
            if state_key not in visited:
                visited.add(state_key)
                next_g = g + cost
                h = heuristic(next_state)
                next_f = next_g + h
                next_path = path + [(description, next_state, cost)]
                heapq.heappush(
                    frontier, (next_f, next_g, next_state, next_path)
                )

    return None
