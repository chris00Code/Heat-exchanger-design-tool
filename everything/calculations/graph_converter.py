import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class ExNode:
    def __init__(self, name, par):
        self.name = name
        self.par = par


n1 = ExNode("A", 1)
n2 = ExNode("B", 2)
n3 = ExNode("C", 2)
n4 = ExNode("D", 2)
i1 = ExNode("Input1", 1)
i2 = ExNode("Input2", 2)

# bsp1
nodes = [n4, n3, n2, n1]
inputs = [i1, i2]
path1 = [(n3, n2), (n2, n1), (n1, n4),(i1,n3)]
path2 = [(n1, n2), (n2, n3), (n3, n4),(i2,n1)]
"""#HUE
nodes=[n1,n2,n3]
path1 = []
path2 = [(n1,n2),(n2,n3)]
#strelow
nodes = [n1,n2,n3,n4]
path1 = [(n1, n2,{'weight': 0.75}), (n1, n3,{'weight': 0.25}), (n2, n4),(n3,n4)]
path2 = [(n2, n1),(n4,n3)]
"""
# Erster Pfad
G1 = nx.DiGraph()
G1.add_nodes_from(inputs)
G1.add_edges_from(path1)
adj_matrix1 = nx.adjacency_matrix(G1, nodelist=nodes).todense()
# Anzeigen der Adjazenzmatrizen
print("Adjazenzmatrix für den ersten Pfad:")
print(adj_matrix1)

inp1 = nx.adjacency_matrix(G1,nodelist=[i1,i2,n1,n2,n3,n4]).todense()
print(inp1)

# Zweiter Pfad
G2 = nx.DiGraph()
G2.add_nodes_from(nodes)
G2.add_edges_from(path2)
adj_matrix2 = nx.adjacency_matrix(G2, nodelist=nodes).todense()

print("Adjazenzmatrix für den zweiten Pfad:")
print(adj_matrix2)

# Plot des ersten Graphen
plt.figure(figsize=(10, 8))
pos1 = nx.spring_layout(G1)
nx.draw(G1, pos=pos1, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Plot des ersten Graphen")

# Plot des zweiten Graphen
plt.figure(figsize=(10, 8))
pos2 = nx.spring_layout(G2)
nx.draw(G2, pos=pos2, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Plot des zweiten Graphen")

plt.show()

"""import networkx as nx
import json
import matplotlib.pyplot as plt

# Pfad zur JSON-Datei mit dem gespeicherten Graphen
json_file_path = '../editor/1.json'

# JSON-Datei laden
with open(json_file_path, 'r') as file:
    graph_data = json.load(file)


def get_input_id(start_id):
    edges = graph_data['edges']

    end_ids = []
    for edge in edges:
        if edge["start"] == start_id:
            end_ids.append(edge["end"])
    return end_ids


def get_node_id(id):
    nodes = graph_data['nodes']

    for node in nodes:
        for input in node["inputs"]:
            if input["id"] == id:
                return node["id"]


flows = []
for node in graph_data["nodes"]:
    if node["title"] == "Input Flow":
        flows.append(node)

for flow in flows:
    print(flow)
    node_list = []
    outputs = flow['outputs']
    current_node_id = flow['id']
    for output in outputs:
        next_input_id = get_input_id(output["id"])
        next_node_id = get_node_id(next_input_id[0])
        node_list.append((current_node_id, next_node_id))
    current_node_id = next_node_id


    print(node_list)"""

"""
G = nx.MultiGraph()

# Hinzufügen der Knoten zum Graphen
#for node in graph_data["nodes"]:
#    G.add_node(node["title"])
#    G.add_node(node["id"], title=node["title"], pos=(node["pos_x"], node["pos_y"]))

# Hinzufügen der Kanten zum Graphen
for edge in graph_data["edges"]:
    G.add_edge(edge["start"], edge["end"])

# Fruchterman-Reingold-Layout verwenden
pos = nx.spring_layout(G)

# Graphen plotten
plt.figure(figsize=(10, 8))
nx.draw(G, pos=pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Plot des Graphen")

# Den Plot anzeigen
plt.show()
"""
