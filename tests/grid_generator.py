from src.display.visualizer import PuzzleVisualizer
from src.grid.grid import generate_puzzle


def test_grid_5x5():
    grid = generate_puzzle(5, 5)
    print("Grille 5x5 générée:")
    for row in grid:
        print(row)
    visualizer = PuzzleVisualizer(grid)
    visualizer.run()
