import networkx as nx
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


    print(node_list)
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
