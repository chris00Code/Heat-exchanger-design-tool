import json
import os.path
from os import path

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, title: str = "Node", node_id: hex = None, flow_ids: list = [], input_ids: list = [],
                 output_ids: list = [],
                 parameters: dict = {}):
        self._title = title
        self._op_code = self.set_op_code()
        self._node_id = node_id
        self._flow_ids = flow_ids
        self._input_ids = input_ids
        self._output_ids = output_ids
        self._parameters = parameters

    def __str__(self):
        return "%s_%s>" % (self.title, self.node_id)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def op_code(self):
        return self._op_code

    def set_op_code(self):
        match self.title:
            case "input":
                value = 0
            case "output":
                value = 1
            case _:
                value = 2
        return value

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        self._node_id = value

    @property
    def flow_ids(self):
        return self._flow_ids

    @flow_ids.setter
    def flow_ids(self, value):
        self._flow_ids = value

    @property
    def output_ids(self):
        return self._output_ids

    @output_ids.setter
    def output_ids(self, value):
        self._output_ids = value

    @property
    def input_ids(self):
        return self._input_ids

    @output_ids.setter
    def input_ids(self, value):
        self._input_ids = value

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value


class GraphRepresentation:
    allowed_formats = ['.json']

    def __init__(self, file_path: str):
        abs_path = path.abspath(file_path)
        root, ext = os.path.splitext(abs_path)
        if ext not in self.allowed_formats:
            raise ValueError("false file type")
        with open(abs_path, 'r') as file:
            self._data = json.load(file)

        self._nodes = self._create_nodes()
        self._paths = self._create_paths()

    @property
    def data(self):
        return self._data

    @property
    def nodes(self):
        return self._nodes

    def _create_nodes(self):
        data = self.data
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
            graph_node = Node(title, node["id"], flow_ids, node["input_ids"], node["output_ids"], node["content"])
            graph_nodes.append(graph_node)
        return sorted(graph_nodes, key=lambda x: x.op_code)

    @property
    def input_nodes(self):
        return [node for node in self.nodes if node.op_code == 0]

    @property
    def output_nodes(self):
        return [node for node in self.nodes if node.op_code == 1]

    @property
    def exchanger_nodes(self):
        return [node for node in self.nodes if node.op_code > 1]

    def get_node_by_id(self, id):
        if id is None:
            return None
        for node in self.nodes:
            if node.node_id == id:
                return node
        return None

    @property
    def paths(self):
        return self._paths

    """
    def _create_paths(self):
        paths = []
        input_nodes = self.input_nodes
        for input in input_nodes:
            flow_id = input.node_id
            path = []
            current_node = input
            next_node = self.get_node_by_id(input.output_ids["1"])
            while next_node is not None:
                connection = (current_node, next_node)
                path.append(connection)
                current_node = next_node
                # when not output
                if current_node._op_code != 1:
                    if current_node.flow_ids["1"] == flow_id:
                        next_node = self.get_node_by_id(current_node.output_ids["1"])
                    elif current_node.flow_ids["2"] == flow_id:
                        next_node = self.get_node_by_id(current_node.output_ids["2"])
                    else:
                        raise ValueError("Input/Output Flows of Node don't match")
                else:
                    next_node = None
            paths.append(path)
        return paths
    """

    def _create_paths(self):
        ex_nodes = self.exchanger_nodes
        paths = {"11": [], "12": [], "21": [], "22": []}
        for node in ex_nodes:
            cur_node_id = node.node_id
            cur_in_ids = node.input_ids
            for i, id in enumerate(cur_in_ids.values()):
                prev_node = self.get_node_by_id(id)
                prev_out_ids = prev_node.output_ids
                type = None
                if i == 0:
                    if cur_node_id == prev_out_ids['1']:
                        type = "11"
                    elif cur_node_id == prev_out_ids['2']:
                        type = "12"
                elif i == 1:
                    if cur_node_id == prev_out_ids['1']:
                        type = "21"
                    elif cur_node_id == prev_out_ids['2']:
                        type = "22"
                if type is not None:
                    edge = (prev_node, node)
                    paths[type].append(edge)
        return paths


if __name__ == "__main__":
    graph_rep = GraphRepresentation("../node_editor/bsp1.json")
    print(graph_rep)
    print(graph_rep.paths)
    nodes = graph_rep.nodes
    ex_nodes = graph_rep.exchanger_nodes
    paths = graph_rep.paths

    G1 = nx.DiGraph()
    G1.add_nodes_from(nodes)
    G1.add_edges_from(paths[0])

    ad = nx.adjacency_matrix(G1, nodelist=nodes).todense()
    print(ad)
    ad_ex = nx.adjacency_matrix(G1, nodelist=ex_nodes).todense()
    print(ad_ex)
