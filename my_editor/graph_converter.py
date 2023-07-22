import networkx as nx
import json
import matplotlib.pyplot as plt
from graph_node import GraphNode

# Pfad zur JSON-Datei mit dem gespeicherten Graphen
json_file_path = 'test.json'

# JSON-Datei laden
with open(json_file_path, 'r') as file:
    graph_data = json.load(file)


def get_nodes(data):
    nodes = [node["id"] for node in data["nodes"]]
    return nodes


def get_node_ids(data):
    return [node["id"] for node in data["nodes"]]


def create_graph_nodes(data):
    grap_nodes = []
    for node in data["nodes"]:
        op_code = node["op_code"]
        match op_code:
            case 1:
                grap_node = GraphNode("input", node["id"], [], node["children_ids"], node["content"])
            case 2:
                grap_node = GraphNode("output", node["id"], [], node["children_ids"], node["content"])
            case 3:
                grap_node = GraphNode("cocurrent", node["id"], [], node["children_ids"], node["content"])
        grap_nodes.append(grap_node)
    return grap_nodes


def get_paths(nodes):
    paths = []
    for input in get_input_nodes(nodes):
        current_node = input
        next_node_id = input.output_ids[0]
        while next_node_id is not None:
            next_node = get_node_by_id(nodes, next_node_id)
            edge = (current_node, next_node)
            paths.append(edge)
            current_node = next_node
            try:
                next_node_id = current_node.output_ids[-1]
            except IndexError:
                next_node_id = None
    return paths


def get_input_nodes(nodes):
    return [node for node in nodes if node.title == "input"]


def get_node_by_id(nodes, id):
    for node in nodes:
        if node.node_id == id:
            return node
    return None


graph_nodes = create_graph_nodes(graph_data)
input_nodes = get_input_nodes(graph_nodes)
paths = get_paths(graph_nodes)

G1 = nx.DiGraph()
G1.add_nodes_from(graph_nodes)
G1.add_edges_from(paths)

# Plot des ersten Graphen
plt.figure(figsize=(10, 8))
pos1 = nx.spring_layout(G1)
nx.draw(G1, pos=pos1, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Plot des ersten Graphen")
plt.show()
