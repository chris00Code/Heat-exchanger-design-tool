from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from calc_conf import register_node, OP_NODE_OUTPUT
from flow_node_base import FlowNode, FlowGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QDoubleValidator
from flow import Flow
from PyQt5 import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit


class FlowOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid_layout)

        font1 = QtGui.QFont()
        font1.setPointSize(11)
        font1.setBold(True)

        label_1 = QLabel("Fluids:")
        label_1.setFont(font1)
        self.grid_layout.addWidget(label_1, 0, 0, 1, 2)

        label_2 = QLabel("fluid:")
        self.grid_layout.addWidget(label_2, 1, 0, 1, 1)

        self.label_3 = QLabel("", self)
        self.label_3.setObjectName(self.node.content_label_objname)
        self.grid_layout.addWidget(self.label_3, 1, 1, 1, 1)

        # Setze den vertikalen Streckfaktor der dritten Zeile auf 1, um den verfügbaren Platz zu nutzen
        self.grid_layout.setRowStretch(2, 1)

@register_node(OP_NODE_OUTPUT)
class FlowNodeOutput(FlowNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "output flow"
    content_label_objname = "flow_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])
        self.flow = None
        self.markDirty()

    def initInnerClasses(self):
        self.content = FlowOutputContent(self)
        self.grNode = FlowGraphicsNode(self)
        self.grNode.height_in = 70


    def evalImplementation(self):
        input = self.getInputWithSocketIndex(0)

        # @TODO implement diversification of flows when same fluids
        if not any(item is None for item in input):
            self.flow = input[0].get_flow(input[1])
            fluid = self.flow.fluid
            self.content.label_3.setText(fluid)

            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()
        else:
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect input")
            self.content.label_3.setText("")
