from collections import deque
import sys
import os
import subprocess
import shutil


def process_file(filename: str) -> dict:
	with open(filename) as f:
		graph = dict()
		for line in f:
			node, edges_list = line.strip().split(":")
			edge_list = [e.strip() for e in edges_list.split() if e]
			if node in graph:
				graph[node] += edge_list
			else:
				graph[node] = edge_list
		return graph


def part_2(graph: dict) -> int:
	"""
	Part_2 minimal (aucun cycle attendu) :
	- effectue Kahn pour obtenir un ordre topologique sur tous les nœuds
	- exécute des DP (forward/backward) et DP depuis 'fft' (fft avant dac toujours)
	"""
	# collect all nodes
	nodes = set(graph.keys())
	for nbrs in graph.values():
		nodes.update(nbrs)

	if 'svr' not in nodes or 'out' not in nodes:
		return 0

	# build adjacency for all nodes (missing keys -> empty list)
	adj_all = {u: list(graph.get(u, [])) for u in nodes}

	# Kahn topological sort on full node set (on suppose le graphe acyclique)
	indeg = {u: 0 for u in nodes}
	for u, nbrs in adj_all.items():
		for v in nbrs:
			indeg[v] += 1
	q = deque([u for u, d in indeg.items() if d == 0])
	topo = []
	while q:
		u = q.popleft()
		topo.append(u)
		for v in adj_all[u]:
			indeg[v] -= 1
			if indeg[v] == 0:
				q.append(v)

	# # si topo ne couvre pas tous les nœuds, on échoue (cycles non attendus)
	# if len(topo) != len(nodes):
	# 	raise ValueError('Cycle détecté dans le graphe (non attendu)')

	# map positions et listes d'adjacence par indices (sur topo)
	pos = {u: i for i, u in enumerate(topo)}
	adj_idx = [[pos[v] for v in adj_all[u]] for u in topo]
	n = len(topo)

	# DP forward depuis 'svr'
	dp_from_s = [0] * n
	dp_from_s[pos['svr']] = 1
	for i in range(n):
		val = dp_from_s[i]
		if val:
			for j in adj_idx[i]:
				dp_from_s[j] += val

	# DP backward vers 'out'
	dp_to_t = [0] * n
	dp_to_t[pos['out']] = 1
	for i in range(n - 1, -1, -1):
		for j in adj_idx[i]:
			dp_to_t[i] += dp_to_t[j]

	# DP depuis fft (fft est toujours avant dac selon la visualisation)
	start_f = pos['fft']
	dp_from_f = [0] * n
	dp_from_f[start_f] = 1
	for i in range(start_f, n):
		if dp_from_f[i]:
			for j in adj_idx[i]:
				dp_from_f[j] += dp_from_f[i]

	paths_f_to_d = dp_from_f[pos['dac']]

	# combine: only fft -> dac order is possible
	res = dp_from_s[pos['fft']] * paths_f_to_d * dp_to_t[pos['dac']]
	return res


# --- Visualisation helpers ---

def _write_dot(graph: dict, path: str, directed: bool = True) -> None:
	"""
	Écrit le graphe au format DOT dans `path`. Colorie les nœuds `svr`, `dac`, `fft`, `out`.
	"""
	kind = 'digraph' if directed else 'graph'
	arrow = '->' if directed else '--'
	# mapping simple de couleur pour Graphviz
	color_map = {'svr': 'red', 'dac': 'orange', 'fft': 'green', 'out': 'blue'}
	with open(path, 'w') as f:
		f.write(f"{kind} G {{\n")
		# nodes (inclure aussi les voisins qui ne seraient pas en tant que clés)
		nodes = set(graph.keys())
		for edges in graph.values():
			nodes.update(edges)
		for node in sorted(nodes):
			if node in color_map:
				f.write(f'  "{node}" [style=filled, fillcolor="{color_map[node]}", color="black"];\n')
			else:
				f.write(f'  "{node}";\n')
		# edges
		for node, edges in graph.items():
			for e in edges:
				f.write(f'  "{node}" {arrow} "{e}";\n')
		f.write('}\n')


def draw_graph(graph: dict, dotfile: str = 'graph.dot', pngfile: str = 'graph.png', view: bool = False) -> str:
	"""
	Génère une visualisation du graphe. Colorie les nœuds spéciaux (`svr`,`dac`,`fft`,`out`) et
	surligne en couleur les chemins "retenus" (svr -> ... -> fft -> ... -> dac -> ... -> out).
	"""
	# couleurs pour matplotlib
	highlight_colors = {'svr': 'red', 'dac': 'orange', 'fft': 'green', 'out': 'blue'}

	# --- helper: compute highlighted nodes and edges ---
	def _compute_highlight(graph):
		# full node set
		nodes = set(graph.keys())
		for nbrs in graph.values():
			nodes.update(nbrs)
		# adjacency and reverse
		adj = {u: list(graph.get(u, [])) for u in nodes}
		rev = {u: [] for u in nodes}
		for u, nbrs in adj.items():
			for v in nbrs:
				rev[v].append(u)

		from collections import deque
		# forward reachable from a start
		def forward(start):
			q = deque([start])
			seen = set()
			while q:
				u = q.popleft()
				if u in seen:
					continue
				seen.add(u)
				for v in adj.get(u, []):
					if v not in seen:
						q.append(v)
			return seen

		# backward reachable to a target (nodes that can reach target)
		def backward(target):
			q = deque([target])
			seen = set()
			while q:
				u = q.popleft()
				if u in seen:
					continue
				seen.add(u)
				for p in rev.get(u, []):
					if p not in seen:
						q.append(p)
			return seen

		# ensure special nodes exist
		if 'svr' not in nodes or 'fft' not in nodes or 'dac' not in nodes or 'out' not in nodes:
			return set(), set()

		# A: nodes on some path svr -> fft  (reachable from svr and can reach fft)
		from_s = forward('svr')
		to_fft = backward('fft')
		A = from_s & to_fft
		# B: nodes on some path fft -> dac
		from_fft = forward('fft')
		to_dac = backward('dac')
		B = from_fft & to_dac
		# C: nodes on some path dac -> out
		from_dac = forward('dac')
		to_out = backward('out')
		C = from_dac & to_out

		nodes_h = A | B | C
		# edges: keep edges whose both endpoints are in nodes_h and are oriented forward
		edges_h = set()
		# compute topological order to ensure direction (fall back to index by arbitrary order)
		pos = {n: i for i, n in enumerate(nodes)}
		for u in nodes:
			for v in adj.get(u, []):
				if u in nodes_h and v in nodes_h:
					edges_h.add((u, v))
		return nodes_h, edges_h

	# compute highlights
	nodes_h, edges_h = _compute_highlight(graph)

	# Tentative networkx + matplotlib
	try:
		import networkx as nx
		import matplotlib.pyplot as plt
		G = nx.DiGraph()
		# add edges; this will also add nodes for endpoints
		for u, nbrs in graph.items():
			for v in nbrs:
				G.add_edge(u, v)
		# ensure isolated keys are also nodes
		for u in graph.keys():
			G.add_node(u)
		# build node list and base colors
		node_list = list(G.nodes())
		node_colors = []
		for n in node_list:
			if n in highlight_colors:
				node_colors.append(highlight_colors[n])
			elif n in nodes_h:
				node_colors.append('#ffff99')  # light yellow for path nodes
			else:
				node_colors.append('#cccccc')

		plt.figure(figsize=(12, 8))
		pos = nx.spring_layout(G, seed=42)
		# draw all nodes
		nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_colors, node_size=500)
		# draw regular edges faintly
		nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=8, edge_color='#999999')
		# draw highlighted edges thicker and colored
		high_edge_list = [e for e in G.edges() if (e[0], e[1]) in edges_h]
		if high_edge_list:
			nx.draw_networkx_edges(G, pos, edgelist=high_edge_list, arrows=True, arrowstyle='->', arrowsize=10, edge_color='red', width=2)
		# labels
		nx.draw_networkx_labels(G, pos, font_size=8)
		# legend
		from matplotlib.patches import Patch
		legend_elems = [Patch(facecolor=c, edgecolor='black', label=label) for label, c in highlight_colors.items()]
		legend_elems.append(Patch(facecolor='#ffff99', edgecolor='black', label='chemins retenus'))
		plt.legend(handles=legend_elems, loc='upper right')
		plt.axis('off')
		plt.tight_layout()
		plt.savefig(pngfile, dpi=150)
		if view:
			plt.show()
		return os.path.abspath(pngfile)
	except Exception:
		# fallback to DOT + Graphviz; write highlighted nodes and edges
		dot_path = dotfile
		kind = 'digraph'
		arrow = '->'
		color_map = {'svr': 'red', 'dac': 'orange', 'fft': 'green', 'out': 'blue'}
		with open(dot_path, 'w') as f:
			f.write(f"{kind} G {{\n")
			# nodes
			nodes = set(graph.keys())
			for edges in graph.values():
				nodes.update(edges)
			for node in sorted(nodes):
				attrs = []
				if node in color_map:
					attrs.append(f'style=filled')
					attrs.append(f'fillcolor="{color_map[node]}"')
					attrs.append('color="black"')
				elif node in nodes_h:
					attrs.append('style=filled')
					attrs.append('fillcolor="#ffff99"')
				if attrs:
					f.write(f'  "{node}" [{", ".join(attrs)}];\n')
				else:
					f.write(f'  "{node}";\n')
			# edges
			for node, edges in graph.items():
				for e in edges:
					if (node, e) in edges_h:
						f.write(f'  "{node}" {arrow} "{e}" [color="red", penwidth=2];\n')
					else:
						f.write(f'  "{node}" {arrow} "{e}";\n')
			f.write('}\n')
		# try to render with dot
		dot_exec = shutil.which('dot')
		if dot_exec:
			try:
				subprocess.run([dot_exec, '-Tpng', dot_path, '-o', pngfile], check=True)
				if view:
					if sys.platform == 'darwin':
						subprocess.run(['open', pngfile])
					elif sys.platform == 'win32':
						subprocess.run(['start', pngfile], shell=True)
					else:
						subprocess.run(['xdg-open', pngfile])
				return os.path.abspath(pngfile)
			except Exception:
				return os.path.abspath(dot_path)
		return os.path.abspath(dot_path)


def main() -> None:
	graph = process_file('input.txt')
	print(f"result aoc day 11 - p2: {part_2(graph)}")
	# optionnel: --draw pour générer une image du graphe
	if '--draw' in sys.argv:
		out = draw_graph(graph, dotfile='graph.dot', pngfile='graph.png', view='--view' in sys.argv)
		print('Graph output:', out)


if __name__ == "__main__":
	main()
