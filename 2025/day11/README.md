# Qu'est‑ce qu'un DAG ?

DAG = Directed Acyclic Graph (en français « graphe orienté acyclique »).
C'est un graphe orienté dans lequel il n'existe aucun cycle orienté (aucun chemin dirigé qui part d'un nœud et revient à ce même nœud).
Intuitivement, c'est une structure de dépendances « sans boucle » : utile pour ordonner des tâches, représenter des pipelines, ou toute relation de précédence.

---

## Propriétés importantes

- Existence d'un ordre topologique : on peut ordonner les nœuds de sorte que chaque arête a→b va d'un indice plus petit vers un indice plus grand.
- Un graphe orienté est un DAG ssi il n'a pas de cycle orienté. La détection d'un cycle empêche l'utilisation directe d'algorithmes qui supposent acyclicité.
- Sur un DAG, de nombreux problèmes deviennent simples et efficaces (souvent O(|V| + |E|)) : comptage de chemins, plus long chemin (si pondéré), planification, etc.

---

## Algorithmes usuels

- Kahn (BFS) : calcul de l'ordre topologique en utilisant les degrés entrants. Si, à la fin, tous les nœuds ont été extraits, le graphe est acyclique. Complexité : O(|V| + |E|).
- DFS (par marquage blanc/gris/noir) : on calcule un ordre topologique par post‑ordre DFS ; la découverte d'un arrière‑arc signale un cycle.
- Compression SCC : sur un graphe qui contient des cycles, on peut compresser les composantes fortement connexes (SCC) en nœuds pour obtenir un DAG des composants.

---

## Pourquoi l'utiliser ici ?

Dans ce projet (analyse de graphes de connexions), on exploite souvent ce pattern :
1. si des cycles existent, compresser en SCC pour obtenir un DAG;
2. effectuer un ordre topologique sur le DAG;
3. appliquer de la programmation dynamique (DP) le long de cet ordre pour compter/agréger des valeurs.

Cette approche évite l'explosion combinatoire lors d'explorations naïves de tous les chemins.

---

## Programmation dynamique (DP) sur DAG — principe

La DP sur un DAG repose sur deux propriétés :
- sub‑problèmes recouvrants (on réutilise des résultats intermédiaires) ;
- optimal substructure (la solution globale se compose de solutions optimales locales).

Exemple typique : compter le nombre de chemins depuis une source `src` vers chaque nœud `u`.
On définit l'état : `dp[u] = nombre de chemins src -> u`.
On initialise `dp[src] = 1` puis, dans l'ordre topologique, on propage :

```
for u in topo:
    for v in adj[u]:
        dp[v] += dp[u]
```

Complexité : O(|V| + |E|) en temps, O(|V|) en mémoire.

---

## Exemple concret (Python)

Le petit extrait ci‑dessous montre un `topo_kahn` et un `count_paths` utilisable directement sur des dictionnaires d'adjacence :

```python
from collections import deque

def topo_kahn(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] = indeg.get(v, 0) + 1
    q = deque([u for u, d in indeg.items() if d == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj.get(u, ()):  # successeurs
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(indeg):
        raise ValueError('Cycle détecté')
    return order

def count_paths(adj, src, dst):
    order = topo_kahn(adj)
    dp = {u: 0 for u in order}
    dp[src] = 1
    for u in order:
        for v in adj.get(u, ()): 
            dp[v] += dp[u]
    return dp[dst]
```

Ce code est déjà adapté à l'approche utilisée par `aoc_day11.py` : on peut d'abord compresser des SCC si nécessaire, puis exécuter cette DP sur le DAG obtenu.

---

## Conseils pratiques

- Si le nombre de chemins devient astronomique et que vous n'avez besoin que d'un résultat modulo M, faites tout le DP modulo M pour limiter la taille des entiers.
- Si le DAG filtré est massif mais traversé par des frontières étroites, pensez à segmenter le calcul par frontières (vecteurs de taille |frontier|) pour gagner en mémoire et CPU.
- Utilisez `networkx` pour prototyper (`nx.topological_sort`, `nx.is_directed_acyclic_graph`), mais préférez des listes d'adjacence et du Python pur pour la performance sur de grands graphes.

---

## Références rapides

- Kahn, A. B. — topological sorting algorithm.
- Tarjan — SCC (pour compression en DAG de composantes).
- NetworkX documentation: https://networkx.org

---

