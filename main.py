from datetime import datetime

from src.grid import generate_puzzle
from src.solver import (
    a_star_solver,
    enhanced_heuristic,
    is_final,
    transformations,
)
from src.visualizer import PuzzleVisualizer


def main():
    # Taille de la grille
    row, col = 5, 5

    # Génération d'un puzzle
    initial_grid = generate_puzzle(row, col)
    print("Génération d'un puzzle:")
    for row in initial_grid:
        print(row)

    # Affichage initial
    print("\nAffichage du puzzle initial :")
    visualizer = PuzzleVisualizer(initial_grid)
    visualizer.run()

    # Résolution avec A*
    print("\nRecherche d'une solution...")
    start_time = datetime.now()

    solution = a_star_solver(
        transformations=transformations,
        isFinal=is_final,
        state=initial_grid,
        heuristic=enhanced_heuristic,
        max_depth=100000,
    )

    end_time = datetime.now()
    print(f"Temps de résolution: {end_time - start_time}")

    # Affichage de la solution
    if solution:
        final_state = solution[-1][1]
        print("Solution du puzzle :")
        for row in final_state:
            print(row)

        print("\nAffichage de la solution:")
        visualizer = PuzzleVisualizer(final_state)
        visualizer.run()
    else:
        print("\nAucune solution trouvée.")


if __name__ == "__main__":
    main()
