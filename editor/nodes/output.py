from qtpy.QtWidgets import QVBoxLayout, QLabel
from qtpy.QtCore import Qt
from calc_conf import register_node, OP_NODE_OUTPUT
from calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from qtpy.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.fluid = QLabel("", self)
        self.fluid.setAlignment(Qt.AlignLeft)
        self.fluid.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.fluid)

        self.temp = QLabel("", self)
        self.temp.setAlignment(Qt.AlignLeft)
        self.temp.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.temp)

        self.dm = QLabel("", self)
        self.dm.setAlignment(Qt.AlignLeft)
        self.dm.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.dm)


@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height = 100

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        fluid = input_node.content.edit_fluid.text()
        temp = input_node.content.edit_temp.text()
        dm = input_node.content.edit_dm.text()

        self.content.fluid.setText(f"Fluid: {fluid}")
        self.content.temp.setText(f"Temperature: {temp} K")
        self.content.dm.setText(f"Mass flow rate: {dm} kg/s")

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return None


"""
class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        self.content.lbl.setText("%d" % val)
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val
"""
