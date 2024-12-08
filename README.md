# Connection Game AI

## Structure

```
connection-game-ai/
├── src/
│ ├── grid.py       # Q1: Génération des puzzles solvables
│ ├── solver.py     # Q3-Q6: Algorithme A\* et heuristiques
│ └── visualizer.py # Q2: Interface graphique avec Pygame
├── shared/
│ └── assets/       # Images des tuiles
└── main.py         # Point d'entrée

```

## Installation

1. Cloner le dépôt
2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Se placer sur la branche principale `v1-main`

```bash
git checkout v1-main
```

## Utilisation

Lancer le programme :

```bash
python main.py
```

## Exemple d'exécution

1. On choisit une grille de taille :

```
row, col = 6, 7
```

2. On génère un puzzle solvable :

![alt text](/shared/assets/image-1.png)

3. L'interface graphique s'ouvre :

![alt text](/shared/assets/image-2.png)

4. On ferme la fenêtre et on obtient la solution :

![alt text](/shared/assets/image-3.png)
![alt text](/shared/assets/image-4.png)

## Auteurs

- Souaibou Dine BARRY (@dineproject from github)
- Zayd ADOUAN
