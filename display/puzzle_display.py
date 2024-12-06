import pygame

from core.models.board import Board
from core.models.tile import TileType


class PuzzleDisplay:
    def __init__(self, board: Board, tile_size: int = 60):
        pygame.init()
        self.board = board
        self.tile_size = tile_size
        # Ajout de 30 pixels en hauteur pour le texte
        self.screen = pygame.display.set_mode(
            (board.width * tile_size, board.height * tile_size + 30)
        )
        pygame.display.set_caption("Touner une tuile en cliquant dessus")

        # Initialisation de la police
        self.font = pygame.font.Font(None, 24)

        self.images = {
            TileType.EMPTY: pygame.image.load("shared/assets/vide.png"),
            TileType.CORNER: pygame.image.load("shared/assets/angle.png"),
            TileType.CROSS: pygame.image.load("shared/assets/cross.png"),
            TileType.LINE: pygame.image.load("shared/assets/line.png"),
            TileType.T_SHAPE: pygame.image.load("shared/assets/te.png"),
            TileType.HALF: pygame.image.load("shared/assets/mid.png"),
        }

        for type_, img in self.images.items():
            self.images[type_] = pygame.transform.scale(
                img, (tile_size, tile_size)
            )

    def get_clicked_tile(self, mouse_pos):
        x = mouse_pos[0] // self.tile_size
        y = mouse_pos[1] // self.tile_size
        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            return (x, y)
        return None

    def display(self):
        self.screen.fill((255, 255, 255))

        # Affichage des tuiles
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.board.get_tile((x, y))
                img = self.images[tile.type]
                if tile.type != TileType.EMPTY and tile.type != TileType.CROSS:
                    img = pygame.transform.rotate(img, -tile.rotation)
                self.screen.blit(img, (x * self.tile_size, y * self.tile_size))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click gauche
                        tile_pos = self.get_clicked_tile(event.pos)
                        if tile_pos:
                            tile = self.board.get_tile(tile_pos)
                            if (
                                tile.type != TileType.EMPTY
                                and tile.type != TileType.CROSS
                            ):
                                tile.rotate()
            self.display()
        pygame.quit()
