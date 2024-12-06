from src.display.visualizer import PuzzleVisualizer
from src.grid.grid import generate_puzzle
from src.solver.path_finder import PathFinder


def test_find_solution():
    grid = generate_puzzle(5, 5)
    print("Recherche solution...")
    solution = PathFinder.find_solution(grid)
    if solution:
        print("Solution trouvée!")
        visualizer = PuzzleVisualizer(solution)
        visualizer.run()
