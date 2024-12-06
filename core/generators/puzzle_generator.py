import random
from typing import List, Optional, Tuple

from core.models.board import Board
from core.models.tile import Tile, TileType


def generate_path(board: Board) -> List[Tuple[int, int]]:
    """
    Génère un chemin aléatoire valide sur une grille donnée.
    Le chemin part de (0,0) et va jusqu'à (N-1,M-1) en respectant les règles de déplacement.
    """
    width, height = board.width, board.height
    path = [(0, 0)]
    x, y = 0, 0
    last_direction = None

    while (x, y) != (width - 1, height - 1):
        moves = []

        if x < width - 1 and last_direction != "gauche":
            moves.append((x + 1, y, "droite"))

        if y < height - 1:
            moves.append((x, y + 1, "bas"))

        if x > 0 and y < height - 1 and last_direction != "droite":
            moves.append((x - 1, y, "gauche"))

        if not moves:
            return generate_path(board)

        x, y, last_direction = random.choice(moves)
        path.append((x, y))

    return path


def set_initial_tuiles(board: Board, path: List[Tuple[int, int]]) -> None:
    """Place les tuiles initiales LINE et CORNER le long du chemin généré."""
    for i in range(len(path)):
        current = path[i]

        if i == 0:
            next_pos = path[i + 1]
            tile = (
                Tile(TileType.LINE)
                if next_pos == (1, 0)
                else Tile(TileType.CORNER)
            )

        elif i == len(path) - 1:
            prev = path[i - 1]
            tile = (
                Tile(TileType.LINE)
                if prev[1] == board.height - 1
                else Tile(TileType.CORNER)
            )

        else:
            prev = path[i - 1]
            next_pos = path[i + 1]
            prev_dx = current[0] - prev[0]
            prev_dy = current[1] - prev[1]
            next_dx = next_pos[0] - current[0]
            next_dy = next_pos[1] - current[1]
            tile = (
                Tile(TileType.CORNER)
                if (next_dx, next_dy) != (prev_dx, prev_dy)
                else Tile(TileType.LINE)
            )

        board.set_tile(tile, current)


def add_connections(board: Board, path: List[Tuple[int, int]]) -> None:
    """Ajoute des connexions supplémentaires aux tuiles du chemin selon leurs cases vides adjacentes."""
    for pos in path:
        neighbors = board.get_neighbors(pos)
        empty_neighbors = []

        for n_pos in neighbors:
            if board.get_tile(n_pos).type == TileType.EMPTY:
                empty_neighbors.append(n_pos)

        if len(empty_neighbors) == 1:
            board.set_tile(Tile(TileType.T_SHAPE), pos)
            board.set_tile(Tile(TileType.HALF), empty_neighbors[0])

        elif len(empty_neighbors) == 2:
            board.set_tile(Tile(TileType.CROSS), pos)
            for empty_pos in empty_neighbors:
                board.set_tile(Tile(TileType.HALF), empty_pos)


def fill_empty_spaces(board: Board) -> None:
    """Remplit les espaces vides restants avec des motifs prédéfinis 3x3."""

    def is_empty_square_3x3(x: int, y: int) -> bool:
        if x + 2 >= board.width or y + 2 >= board.height:
            return False
        for i in range(3):
            for j in range(3):
                if board.get_tile((x + i, y + j)).type != TileType.EMPTY:
                    return False
        return True

    def fill_pattern_1(x: int, y: int):
        board.set_tile(Tile(TileType.CORNER), (x, y))
        board.set_tile(Tile(TileType.T_SHAPE), (x + 1, y))
        board.set_tile(Tile(TileType.CORNER), (x + 2, y))
        board.set_tile(Tile(TileType.T_SHAPE), (x, y + 1))
        board.set_tile(Tile(TileType.CROSS), (x + 1, y + 1))
        board.set_tile(Tile(TileType.T_SHAPE), (x + 2, y + 1))
        board.set_tile(Tile(TileType.CORNER), (x, y + 2))
        board.set_tile(Tile(TileType.T_SHAPE), (x + 1, y + 2))
        board.set_tile(Tile(TileType.CORNER), (x + 2, y + 2))

    def fill_pattern_2(x: int, y: int):
        board.set_tile(Tile(TileType.HALF), (x, y))
        board.set_tile(Tile(TileType.LINE), (x + 1, y))
        board.set_tile(Tile(TileType.HALF), (x + 2, y))
        board.set_tile(Tile(TileType.CORNER), (x, y + 1))
        board.set_tile(Tile(TileType.T_SHAPE), (x + 1, y + 1))
        board.set_tile(Tile(TileType.CORNER), (x + 2, y + 1))
        board.set_tile(Tile(TileType.CORNER), (x, y + 2))
        board.set_tile(Tile(TileType.CORNER), (x + 1, y + 2))
        board.set_tile(Tile(TileType.HALF), (x + 2, y + 2))

    for y in range(board.height - 2):
        for x in range(board.width - 2):
            if is_empty_square_3x3(x, y):
                (
                    fill_pattern_1(x, y)
                    if random.choice([True, False])
                    else fill_pattern_2(x, y)
                )


def randomize_rotations(board: Board) -> None:
    """Applique des rotations aléatoires aux tuiles sauf EMPTY et CROSS."""
    for y in range(board.height):
        for x in range(board.width):
            tile = board.get_tile((x, y))
            if tile.type not in [TileType.EMPTY, TileType.CROSS]:
                tile.rotate(random.randint(0, 3))


def generate_puzzle(width: int, height: int) -> Board:
    """Génère un puzzle complet selon les dimensions spécifiées."""
    board = Board(width, height)
    path = generate_path(board)
    set_initial_tuiles(board, path)
    add_connections(board, path)
    fill_empty_spaces(board)
    randomize_rotations(board)
    return board
