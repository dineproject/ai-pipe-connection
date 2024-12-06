import pygame

from src.display.visualizer import PuzzleVisualizer
from src.grid.grid import generate_puzzle


def main():
    width, height = 5, 6

    # Génération puzzle
    grid = generate_puzzle(width, height)
    print(f"Puzzle {width}x{height} généré")
    visualizer = PuzzleVisualizer(grid)
    visualizer.run()


if __name__ == "__main__":
    main()
