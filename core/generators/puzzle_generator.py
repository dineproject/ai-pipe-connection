import random
from typing import List, Optional, Tuple

from core.models.board import Board
from core.models.tile import Tile, TileType


def generate_path(board: Board) -> List[Tuple[int, int]]:
    """
    Génère un chemin aléatoire valide sur une grille donnée

    Args:
        board: Le plateau de jeu
    Returns:
        List[Tuple[int, int]]: Liste des positions du chemin
    """
    width, height = board.width, board.height
    path = [(0, 0)]
    x, y = 0, 0
    last_direction = None

    while (x, y) != (width - 1, height - 1):
        moves = []

        # Droite (si pas venu de gauche)
        if x < width - 1 and last_direction != "gauche":
            moves.append((x + 1, y, "droite"))

        # Bas (toujours possible)
        if y < height - 1:
            moves.append((x, y + 1, "bas"))

        # Gauche (si pas venu de droite et pas sur dernière ligne)
        if x > 0 and y < height - 1 and last_direction != "droite":
            moves.append((x - 1, y, "gauche"))

        if not moves:
            return generate_path(board)

        x, y, last_direction = random.choice(moves)
        path.append((x, y))

    return path


def set_initial_tuiles(board: Board, path: List[Tuple[int, int]]) -> None:
    """
    Placement initial des tuiles simples (LINE et CORNER) le long du chemin
    """
    for i in range(len(path)):
        current = path[i]

        # Pour la première tuile
        if i == 0:
            next_pos = path[i + 1]
            if next_pos == (1, 0):
                tile = Tile(TileType.LINE)
            else:
                tile = Tile(TileType.CORNER)

        # Pour la dernière tuile
        elif i == len(path) - 1:
            prev = path[i - 1]
            if prev[1] == board.height - 1:
                tile = Tile(TileType.LINE)
            else:
                tile = Tile(TileType.CORNER)

        # Pour les tuiles du milieu
        else:
            prev = path[i - 1]
            next_pos = path[i + 1]

            prev_dx = current[0] - prev[0]
            prev_dy = current[1] - prev[1]
            next_dx = next_pos[0] - current[0]
            next_dy = next_pos[1] - current[1]

            if (next_dx, next_dy) != (prev_dx, prev_dy):
                tile = Tile(TileType.CORNER)
            else:
                tile = Tile(TileType.LINE)

        board.set_tile(tile, current)


def add_connections(board: Board, path: List[Tuple[int, int]]) -> None:
    """
    Ajoute des connections supplémentaires le long du chemin.
    Pour chaque position du chemin:
    - Si 1 case vide adjacente: remplace par T_SHAPE + HALF
    - Si 2 cases vides adjacentes: remplace par CROSS + 2 HALF
    - Si 0 case vide: garde la tuile existante

    Args:
        board: Le plateau de jeu
        path: Liste des positions formant le chemin
    """
    for pos in path:
        # Identifie les cases vides parmi les voisins
        neighbors = board.get_neighbors(pos)
        empty_neighbors = []

        for n_pos in neighbors:
            if board.get_tile(n_pos).type == TileType.EMPTY:
                empty_neighbors.append(n_pos)

        # Crée une connexion T_SHAPE avec une case vide
        if len(empty_neighbors) == 1:
            board.set_tile(Tile(TileType.T_SHAPE), pos)
            board.set_tile(Tile(TileType.HALF), empty_neighbors[0])

        # Crée une connexion CROSS avec deux cases vides
        elif len(empty_neighbors) == 2:
            board.set_tile(Tile(TileType.CROSS), pos)
            for empty_pos in empty_neighbors:
                board.set_tile(Tile(TileType.HALF), empty_pos)


def fill_empty_spaces(board: Board) -> None:
    """
    Remplit les cases vides restantes sur le plateau.
    Pour chaque case vide:
    - Si 2 cases vides adjacentes en angle droit: place CORNER + 2 HALF
    """
    # Parcours du plateau ligne par ligne
    for y in range(board.height):
        for x in range(board.width):
            current = (x, y)
            # Vérifie si la case actuelle est vide
            if board.get_tile(current).type == TileType.EMPTY:
                # Trouve les voisins vides
                neighbors = board.get_neighbors(current)
                empty_neighbors = []

                for n_pos in neighbors:
                    if board.get_tile(n_pos).type == TileType.EMPTY:
                        empty_neighbors.append(n_pos)

                # Si exactement 2 voisins vides en angle droit
                if len(empty_neighbors) == 2:
                    x1, y1 = empty_neighbors[0]
                    x2, y2 = empty_neighbors[1]
                    if (
                        abs(x1 - x2) + abs(y1 - y2) == 2
                    ):  # Vérifie l'angle droit
                        board.set_tile(Tile(TileType.CORNER), current)
                        board.set_tile(Tile(TileType.HALF), empty_neighbors[0])
                        board.set_tile(Tile(TileType.HALF), empty_neighbors[1])


def randomize_rotations(board: Board) -> None:
    """
    Applique un nombre aléatoire de rotations à toutes les tuiles du plateau
    sauf les cases vides et les croix.
    """
    for y in range(board.height):
        for x in range(board.width):
            tile = board.get_tile((x, y))
            if tile.type not in [TileType.EMPTY, TileType.CROSS]:
                nb_rotations = random.randint(0, 3)
                tile.rotate(nb_rotations)


def generate_puzzle(width: int, height: int) -> Board:
    """
    Génère un puzzle de taille donnée.
    Args:
        width: Largeur du plateau
        height: Hauteur du plateau
    Returns:
        Board: Le plateau de jeu généré
    """
    board = Board(width, height)
    path = generate_path(board)
    set_initial_tuiles(board, path)
    add_connections(board, path)
    fill_empty_spaces(board)
    randomize_rotations(board)
    return board
