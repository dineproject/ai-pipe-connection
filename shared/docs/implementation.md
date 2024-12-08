# Rapport d'Implémentation - AI Project : The Connection Game

**Note** : Lors de la rédaction et du débogage, nous avons utilisé **ChatGPT** comme outil d'assistance pour corriger nos explications ainsi que pour débugger notre code.

## Table des matières

0. [Lien avec la première partie](#0-lien-avec-la-première-partie)
1. [Structures de données](#1-structures-de-données)
2. [Génération de puzzle (Q1)](#2-génération-de-puzzle-q1)
3. [Visualisation (Q2)](#3-visualisation-q2)
4. [États terminaux et A\* (Q3-Q6)](#4-états-terminaux-et-a-q3-q6)

---

## 0. Lien avec la première partie

Les principales modifications par rapport au premier dépôt sont les suivantes :

- La représentation des tuiles est désormais sous la forme `[haut, droite, bas, gauche]`.
- Deux nouvelles actions ont été ajoutées, en plus de la rotation à droite : **rotation double** et **rotation triple**.
- Une refonte de la fonction heuristique a été réalisée.

---

## 1. Structures de données

### 1.1 Représentation d'une tuile

Une tuile est représentée par une liste de 4 bits indiquant l'état (ouvert/fermé) de chaque côté :

```python
tile = [haut, droite, bas, gauche]  # Liste de 4 bits (0 ou 1)
```

Exemples de types de tuiles possibles :

````python
EMPTY = [0, 0, 0, 0]      # Tuile vide
CROSS = [1, 1, 1, 1]      # Croix (tous les côtés ouverts)
LINE = [0, 1, 0, 1]       # Ligne horizontale
CORNER = [0, 1, 1, 0]     # Coin
T_SHAPE = [1, 1, 1, 0]    # Forme en T
HALF = [1, 0, 0, 0]       # Demi-connexion

### 1.2 Représentation du plateau

Le plateau est une grille 2D de tuiles :

```python
grid = [
    [[0, 1, 0, 1], [1, 0, 0, 1], ...],  # Ligne 0
    [[1, 0, 1, 0], [1, 1, 1, 1], ...],  # Ligne 1
    ...
]
````

---

## 2. Génération de puzzle (Q1)

### 2.1 Approche en 4 étapes

#### a) Génération du chemin valide

```python
def generate_path(board: Board) -> List[Position]:
    """Génère un chemin de (0,0) à (N-1,M-1)"""
    path = [(0, 0)]
    while path[-1] != (N-1, M-1):
        # Choix des mouvements possibles
        moves = get_valid_moves(current, last_direction)
        # Choix aléatoire d'un mouvement
        next_pos = random.choice(moves)
        path.append(next_pos)
```

Contraintes :

- Départ en (0,0)
- Arrivée en (N-1,M-1)
- Mouvements autorisés : droite, bas, gauche
- Pas de mouvement opposé à la direction précédente
- Pas de mouvement gauche sur la dernière ligne

#### b) Placement initial des tuiles

```python
def set_initial_tuiles(board: Board, path: List[Position]):
    """Place les tuiles LINE et CORNER le long du chemin"""
    for i, pos in enumerate(path):
        if i == 0:  # Première tuile
            tile = LINE if path[1] == (1, 0) else CORNER
        elif i == len(path)-1:  # Dernière tuile
            tile = LINE if prev_on_last_row else CORNER
        else:  # Tuiles intermédiaires
            tile = LINE if same_direction else CORNER
        board.set_tile(tile, pos)
```

#### c) Ajout de connexions

```python
def add_connections(board: Board, path: List[Position]):
    """Ajoute des connexions T_SHAPE et CROSS"""
    for pos in path:
        empty_neighbors = count_empty_neighbors(pos)
        if len(empty_neighbors) == 1:
            add_t_shape_connection(pos, empty_neighbors[0])
        elif len(empty_neighbors) == 2:
            add_cross_connection(pos, empty_neighbors)
```

#### d) Finalisation

```python
def randomize_rotations(board: Board):
    """Applique des rotations aléatoires aux tuiles"""
    for tile in board:
        if can_rotate(tile):
            rotations = random.randint(0, 3)
            tile.rotate(rotations)
```

---

## 3. Visualisation (Q2)

### 3.1 Interface Pygame

```python
class PuzzleVisualizer:
    def __init__(self, grid: Grid):
        # Chargement des images
        self.images = {
            "empty": load_image("vide.png"),
            "cross": load_image("cross.png"),
            ...
        }

    def display(self):
        # Affichage des tuiles
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                type, rotation = get_tile_type_and_rotation(tile)
                draw_tile(type, rotation, x, y)
```

### 3.2 Interaction

- **Clic gauche** : fait tourner une tuile
- La rotation est effectuée par décalage cyclique de la liste : `[a, b, c, d] → [d, a, b, c]`

---

## 4. États terminaux et A\* (Q3-Q6)

### 4.1 Vérification d'état terminal

La fonction `is_final` valide une configuration en se basant sur deux critères principaux :

#### a) Vérification des coins et bords

- Analyse des connexions ouvertes sur les tuiles périphériques.
- Contraintes spécifiques selon la position :
  - Coins : limites min/max de connexions ouvertes
  - Bords : validation de l'étanchéité

#### b) Connexions internes

Pour chaque tuile non périphérique :

- Les connexions ouvertes doivent être compatibles avec les tuiles adjacentes.
- Vérification des 4 directions (haut, droite, bas, gauche).

### 4.2 Système de rotations

Trois fonctions permettent d'appliquer des rotations :

```python
def rotation_a_droite(tile):
    """Rotation 90° : [a, b, c, d] → [d, a, b, c]"""

def double_rotation(tile):
    """Rotation 180° : deux rotations simples"""

def triple_rotation(tile):
    """Rotation 270° : trois rotations simples"""
```

### 4.3 Génération des états successeurs

La fonction `transformations` applique des règles spécifiques selon le type de tuile :

- `[0, 0, 0, 0]` et `[1, 1, 1, 1]` : pas de rotation possible.
- Tuiles ligne (`[1, 0, 1, 0]` ou `[0, 1, 0, 1]`) : une rotation possible.
- Autres tuiles : jusqu'à trois rotations possibles.

Chaque configuration générée est une copie de la grille.

### 4.4 Heuristique avancée

L'heuristique combine trois métriques :

1. **Connexions invalides** :

   - Nombre de connexions incompatibles entre les bords adjacents.

2. **Pénalités de bord** :

   - Vérification des contraintes sur les bords du plateau.

3. **Coût de rotation** :
   - Nombre minimal de rotations nécessaires pour améliorer la configuration.

L'heuristique finale est la somme de ces composantes, orientant l'algorithme A\* vers les solutions prometteuses.

---

### Conclusion

Nous avons testé une implémentation avec DFS, mais elle est inefficace dès que la grille dépasse `3x3`. En revanche, A\* avec notre heuristique permet de résoudre des grilles `10x10` rapidement. Cependant, pour des tailles importantes comme `300x300`, l'algorithme devient très lent, indiquant que l'heuristique utilisée peut encore être optimisée.
