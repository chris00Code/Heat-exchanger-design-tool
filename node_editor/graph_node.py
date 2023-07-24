"""
Node:
"title": title ["input", "output", cell"]
"node_id": node_id
"input_nodes_id":
    {
    "1":
    "2":
    }
"outputs_node_id":
    {
    "1":
    "2":
    }
"parameters":
    {
    }
"""


class GraphNode:
    def __init__(self, title: str = "Graph Node", node_id: hex = None, flow_ids: list = [], output_ids: list = [],
                 parameters: dict = {}):
        self._title = title
        self._op_code = self.set_op_code()
        self._node_id = node_id
        self._flow_ids = flow_ids
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
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value
