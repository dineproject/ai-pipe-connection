import os

import pygame

from ..grid.grid import Grid


class PuzzleVisualizer:
    """Interface graphique pour visualiser et manipuler le puzzle"""

    def __init__(self, grid: Grid, tile_size: int = 60):
        """Initialise le visualiseur avec une grille et une taille de tuile"""
        pygame.init()
        self.grid = grid
        self.tile_size = tile_size
        height, width = len(grid), len(grid[0])
        self.screen = pygame.display.set_mode(
            (width * tile_size, height * tile_size)
        )
        pygame.display.set_caption("Visualiseur de puzzle : click pour tourner")

        assets_path = os.path.join("shared", "assets")
        self.images = {
            "empty": self._load_and_scale("vide.png", assets_path),
            "cross": self._load_and_scale("cross.png", assets_path),
            "corner": self._load_and_scale("angle.png", assets_path),
            "line": self._load_and_scale("line.png", assets_path),
            "tshape": self._load_and_scale("te.png", assets_path),
            "half": self._load_and_scale("mid.png", assets_path),
        }

    def _load_and_scale(self, filename: str, path: str) -> pygame.Surface:
        """Charge et redimensionne une image"""
        return pygame.transform.scale(
            pygame.image.load(os.path.join(path, filename)),
            (self.tile_size, self.tile_size),
        )

    def _get_tile_type_and_rotation(self, tile: list) -> tuple[str, int]:
        """Détermine le type et la rotation d'une tuile selon sa configuration"""
        if tile == [0, 0, 0, 0]:
            return "empty", 0
        if tile == [1, 1, 1, 1]:
            return "cross", 0

        if sum(tile) == 3:
            rotations = {
                (1, 1, 1, 0): 0,
                (0, 1, 1, 1): 90,
                (1, 0, 1, 1): 180,
                (1, 1, 0, 1): 270,
            }
            return "tshape", rotations.get(tuple(tile), 0)

        if sum(tile) == 2:
            if tile in [[0, 1, 0, 1], [1, 0, 1, 0]]:
                return "line", 90 if tile[0] == 1 else 0

            corners = {
                (0, 1, 1, 0): 0,
                (0, 0, 1, 1): 90,
                (1, 0, 0, 1): 180,
                (1, 1, 0, 0): 270,
            }
            return "corner", corners.get(tuple(tile), 0)

        if sum(tile) == 1:
            halfs = {
                (1, 0, 0, 0): 270,
                (0, 1, 0, 0): 0,
                (0, 0, 1, 0): 90,
                (0, 0, 0, 1): 180,
            }
            return "half", halfs.get(tuple(tile), 0)

        return "empty", 0

    def get_clicked_position(self, mouse_pos: tuple) -> tuple:
        """Convertit position souris en coordonnées grille"""
        x = mouse_pos[0] // self.tile_size
        y = mouse_pos[1] // self.tile_size
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return (x, y)
        return None

    def display(self):
        """Affiche l'état actuel du puzzle"""
        self.screen.fill((255, 255, 255))
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                tile = self.grid[y][x]
                img_type, rotation = self._get_tile_type_and_rotation(tile)
                img = self.images[img_type]
                if img_type not in ["empty", "cross"]:
                    img = pygame.transform.rotate(img, rotation)
                self.screen.blit(img, (x * self.tile_size, y * self.tile_size))
        pygame.display.flip()

    def run(self):
        """Lance la boucle principale d'affichage et d'interaction"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = self.get_clicked_position(event.pos)
                    if pos:
                        tile = self.grid[pos[1]][pos[0]]
                        if tile != [0, 0, 0, 0] and tile != [1, 1, 1, 1]:
                            self.grid[pos[1]][pos[0]] = tile[-1:] + tile[:-1]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.grid = find_solution(self.grid)
                self.display()
        pygame.quit()
