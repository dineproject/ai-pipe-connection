import heapq
from copy import deepcopy
from typing import List, Optional, Set, Tuple

from .heuristics import advanced_heuristic
from .terminal_checker import is_terminal_state

Grid = List[List[List[int]]]


class PathFinder:
    @staticmethod
    def find_solution(grid: Grid) -> Optional[Grid]:
        """Trouve une solution avec A*."""

        def grid_to_key(g: Grid) -> tuple:
            return tuple(tuple(tuple(tile) for tile in row) for row in g)

        start_h = advanced_heuristic(grid)
        frontier = [(start_h, 0, grid)]
        seen = {grid_to_key(grid)}

        while frontier:
            _, cost, current = heapq.heappop(frontier)

            if is_terminal_state(current):
                return current

            for next_state in PathFinder.get_successors(current):
                key = grid_to_key(next_state)
                if key not in seen:
                    seen.add(key)
                    h = advanced_heuristic(next_state)
                    heapq.heappush(
                        frontier, (cost + 1 + h, cost + 1, next_state)
                    )

        return None

    @staticmethod
    def get_successors(grid: Grid) -> List[Grid]:
        """Génère tous les états possibles après une rotation."""
        successors = []
        height, width = len(grid), len(grid[0])

        for y in range(height):
            for x in range(width):
                tile = grid[y][x]
                if tile == [0, 0, 0, 0] or tile == [1, 1, 1, 1]:
                    continue

                # Rotation de 90°
                new_grid = deepcopy(grid)
                new_grid[y][x] = new_grid[y][x][-1:] + new_grid[y][x][:-1]
                successors.append(new_grid)

        return successors
