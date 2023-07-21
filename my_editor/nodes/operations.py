from calc_conf import register_node, OP_NODE_EX_COUNTER, OP_NODE_EX_CO
from ex_node_base import ExNode


@register_node(OP_NODE_EX_CO)
class ExNode_Co(ExNode):
    icon = "icons/cocurrent.png"
    op_code = OP_NODE_EX_CO
    op_title = "co-current"
    content_label = "->->"
    content_label_objname = "excalc_node_bg"


@register_node(OP_NODE_EX_COUNTER)
class ExNode_Counter(ExNode):
    icon = "icons/countercurrent.png"
    op_code = OP_NODE_EX_COUNTER
    op_title = "counter-current"
    content_label = "<-->"
    content_label_objname = "excalc_node_bg"
