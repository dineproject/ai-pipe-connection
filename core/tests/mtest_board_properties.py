import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.models.board import Board 
from core.models.tile import Direction, Tile, TileType

def test_board_properties():
   """
   Teste les propriétés et méthodes de la classe Board.
   Tests :
   - Création du plateau
   - Placement de tuiles avec différentes rotations
   - Récupération des voisins d'une tuile
   - Vérification du voisinage
   - Affichage du plateau
   """
   # Création d'un plateau 5x6
   board = Board(5, 6)

   # Placement de différentes tuiles avec rotations
   # Tuile en T, position (2,3), rotation 180°
   tile_t = Tile(TileType.T_SHAPE)
   board.set_tile(tile_t, (2, 3))
   tile_t.rotate(2)

   # Tuile corner, position (4,5), rotation 90°
   tile_c = Tile(TileType.CORNER)
   board.set_tile(tile_c, (4, 5))
   tile_c.rotate(1)

   # Tuile ligne, position (0,0)
   tile_l = Tile(TileType.LINE)
   board.set_tile(tile_l, (0, 0))

   # Tuile moitié, position (0,1)
   tile_h = Tile(TileType.HALF)
   board.set_tile(tile_h, (0, 1))

   # Tuile croix, position (1,0)
   tile_c = Tile(TileType.CROSS)
   board.set_tile(tile_c, (1, 0))

   # Test des méthodes get_neighbors et are_neighbors
   neighbors = board.get_neighbors((2, 3))
   print("Voisins de la position (2,3):", neighbors)
   
   print("(2,3) et (3,3) sont voisins:", board.are_neighbors((2, 3), (3, 3)))
   
   # Affichage du plateau
   print("\nÉtat du plateau:")
   print(board)
   print("\n")

if __name__ == "__main__":
   test_board_properties()