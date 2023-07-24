import networkx as nx
import json
import matplotlib.pyplot as plt
from graph_node import GraphNode

# Pfad zur JSON-Datei mit dem gespeicherten Graphen
json_file_path = '3.json'

# JSON-Datei laden
with open(json_file_path, 'r') as file:
    graph_data = json.load(file)


def get_nodes(data):
    nodes = [node["id"] for node in data["nodes"]]
    return nodes


def get_node_ids(data):
    return [node["id"] for node in data["nodes"]]


def create_graph_nodes(data):
    graph_nodes = []
    for node in data["nodes"]:
        op_code = node["op_code"]
        match op_code:
            case 1:
                title = "input"
                flow_ids = None
            case 2:
                title = "output"
                flow_ids = None
            case 3:
                title = "countercurrent"
                flow_ids = node["flow_ids"]
            case 4:
                title = "cocurrent"
                flow_ids = node["flow_ids"]
        graph_node = GraphNode(title, node["id"], flow_ids, node["output_ids"], node["content"])
        graph_nodes.append(graph_node)
    return sorted(graph_nodes, key=lambda x: x._op_code)


def get_input_nodes(nodes):
    return [node for node in nodes if node._op_code == 0]


def get_output_nodes(nodes):
    return [node for node in nodes if node._op_code == 1]


def get_exchanger_nodes(nodes):
    return [node for node in nodes if node._op_code > 1]


def get_node_by_id(nodes, id):
    if id is None:
        return None
    for node in nodes:
        if node.node_id == id:
            return node
    return None


def get_paths(nodes):
    # @TODO implement multiedge and weights
    paths = []
    for input in get_input_nodes(nodes):
        flow_id = input.node_id
        path = []
        current_node = input
        next_node = get_node_by_id(nodes, input.output_ids["1"])
        while next_node is not None:
            connection = (current_node, next_node)
            path.append(connection)
            current_node = next_node
            # when not output
            if current_node._op_code != 1:
                if current_node.flow_ids["1"] == flow_id:
                    next_node = get_node_by_id(nodes, current_node.output_ids["1"])
                elif current_node.flow_ids["2"] == flow_id:
                    next_node = get_node_by_id(nodes, current_node.output_ids["2"])
                else:
                    raise ValueError("Input/Output Flows of Node don't match")
            else:
                next_node = None
        paths.append(path)
    return paths


graph_nodes = create_graph_nodes(graph_data)
input_nodes = get_input_nodes(graph_nodes)
output_nodes = get_output_nodes(graph_nodes)

paths = get_paths(graph_nodes)

G1 = nx.DiGraph()
G1.add_nodes_from(graph_nodes)
G1.add_edges_from(paths[2])

# Plot des ersten Graphen
plt.figure(figsize=(10, 8))
pos1 = nx.spring_layout(G1)
nx.draw(G1, pos=pos1, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Plot des ersten Graphen")
plt.show()
