# Résumé des solutions (Day12)

Ce document résume les deux approches implémentées pour résoudre le problème de placement des formes dans une grille (`/2025/day12/aoc_day12.py`). Les deux implémentations visent à répondre à la même contrainte : pour chaque grille spécifiée, placer toutes les instances demandées de chaque type de forme (A..F), en autorisant les rotations, et déterminer si une solution complète existe.

## Plan bref

- Solution 1 — DFS naïf : backtracking récursif en testant pour chaque instance toutes les positions et rotations possibles.
- Solution 2 — Version optimisée : pré-calcul des placements en bitmasks, heuristique MRV (Most-Restricted Variable), mémoïsation des états échoués et pruning par aire restante.

---

## Fichiers pertinents

- `aoc_day12.py` : implémentation actuelle (contient les deux versions, la version optimisée est utilisée par `part_1`).
- `aoc_day12_naïve.py` : (copie historique / référence) version naïve si présente.
- `input_example.txt`, `input.txt` : jeux de données d'exemple et réels.

---

## 1) Solution initiale — DFS naïf (backtracking simple)

Description

- Pour chaque type de forme et chaque instance requise, le solver parcourt toutes les positions `(x,y)` valides de la grille et toutes les rotations (0°, 90°, 180°, 270°).
- À chaque tentative de placement, on vérifie qu'il n'y a pas de collision avec les formes déjà posées. Si le placement est possible on le pose et on recule récursivement pour placer l'instance suivante.
- Backtracking standard : si une branche n'aboutit pas, on annule le dernier placement et on essaie une autre option.

Caractéristiques

- Facile à comprendre et à implémenter.
- Fonctionne pour des petites grilles / petits nombres d'instances.

Complexité et limites

- Complexité exponentielle (énorme) dans le pire cas. Le nombre d'états est le produit des placements possibles pour chaque instance.
- Devient rapidement impraticable lorsque la grille est grande ou que beaucoup d'instances doivent être placées.

Quand l'utiliser

- Pour prototypage, débogage, ou grilles très petites (exemples pédagogiques).

---

## 2) Solution optimisée — Bitmasks + MRV + Mémoïsation

But

- Rendre la recherche exacte viable sur des cas plus volumineux en réduisant le coût des opérations de vérification et en guidant la recherche.

Étapes principales

1. Pré-calcul des placements possibles : pour chaque type de forme et pour chaque rotation distincte, on calcule la liste de placements valides (position) et on encode chaque placement comme un bitmask entier où chaque bit représente une case de la grille occupée.

2. Représentation par bitmasks : l'état courant de la grille est un entier `occupied` où les bits à 1 représentent les cases déjà utilisées. Tester si une placement `p` recouvre de l'existant devient `if (p & occupied) == 0` (très rapide).

3. Heuristique MRV : à chaque étape on choisit le type de forme (variable) qui a le plus petit nombre d'options de placements valides compte tenu de l'état courant (Most-Restricted Variable). Cela réduit fortement le branching factor.

4. Mémoïsation des états morts : on mémorise dans un set (`seen_fail`) les états `(occupied_bitmask, tuple(counts_restants))` qui ont déjà mené à un échec pour éviter de ré-explorer le même sous-arbre.

5. Pruning par aire : si l'aire totale minimale requise par les instances restantes dépasse le nombre de cases libres, la branche est coupée immédiatement.

6. Reconstruction de la solution : lorsqu'une affectation complète est trouvée on reconstruit la grille finale à partir de la liste des placements choisis.

Avantages

- Opérations d'intersection et d'union très rapides grâce aux opérations bitwise sur int.
- Réduction importante de l'espace d'exploration via MRV et mémoïsation.
- Empirically applicable à des grilles beaucoup plus grandes que la version naïve (mais reste exponentielle en général).

Limitations

- Le nombre total de placements pré-calculés peut être très élevé (par ex. si la grille est grande et la forme petite) et consommer mémoire.
- Dans des cas très denses ou symétriques, l'exploration peut toujours être coûteuse.

---

## Reproduire localement (exemples)

Se placer dans le dossier `2025/day12` et exécuter :

```bash
# tester avec les données d'exemple
python3 - <<'PY'
import time, aoc_day12 as m
s,g = m.process_file('input_example.txt')
start = time.time()
print('result', m.part_1(s,g))
print('time', time.time()-start)
PY
```

```bash
# tester sur input.txt (peut être long selon la taille)
python3 - <<'PY'
import time, aoc_day12 as m
s,g = m.process_file('input.txt')
start = time.time()
print('result', m.part_1(s,g))
print('time', time.time()-start)
PY
```

> Remarque : `part_1` utilise la version optimisée (`solve_grid_full` en bitmask + MRV). Pour comparer avec l'ancienne implémentation naïve, vous pouvez exécuter la version historique `aoc_day12_naïve.py` si elle est disponible.

---

## Résultats sur l'exemple fourni

- Pour `input_example.txt`, la solution optimisée trouve que 2 grilles peuvent être entièrement remplies (valeur attendue) et affiche les plans de remplissage.
- Mesure rapide observée lors d'un test local : ~1.7 s pour l'exemple complet (varie selon la machine).

---

## Recommandations / prochaines étapes

1. Ajouter les flips (miroirs) aux orientations si les formes peuvent être retournées — facile à intégrer lors du pré-calcul des rotations.
2. Implémenter Algorithm X / Dancing Links (DLX) si vous prévoyez des cas beaucoup plus grands et souhaitez la méthode la plus efficace pour ce genre de contraintes couvrantes.
3. Réduire le nombre de placements pré-calculés : filtrer placements symétriques ou dominés, ou appliquer heuristiques de sélection des placements qui couvrent les cases « rares » en priorité.
4. Parallélisation : traiter des grilles indépendantes en parallèle (multiprocessing) ; ou paralléliser la recherche en divisant l'espace des placements d'une variable.
5. Si performance critique : réécrire le noyau en C/Cython pour accélérer les opérations bitwise et les boucles de placement.

---

## Contact / notes de maintenance

- Code principal : `2025/day12/aoc_day12.py`.
- Pour toute modification algorithmique, écrire des tests unitaires qui valident le nombre de grilles remplies sur `input_example.txt` (devrait renvoyer `2`).


---

Fichier généré automatiquement par l'outil d'assistance. Si vous souhaitez que j'ajoute un diagramme visuel (PNG) des grilles solutions ou que j'implémente DLX, dites-moi laquelle des améliorations prioriser et je l'implémente.
