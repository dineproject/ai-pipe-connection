import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from core.generators.puzzle_generator import *
from core.models.board import Board
from core.models.tile import Tile, TileType
from display.puzzle_display import PuzzleDisplay

if __name__ == "__main__":
    board = generate_puzzle(8, 9)
    display = PuzzleDisplay(board)
    display.run()
