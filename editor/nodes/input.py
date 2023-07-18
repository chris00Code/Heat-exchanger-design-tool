from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from calc_conf import register_node, OP_NODE_INPUT
from flow_node_base import FlowNode, FlowGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QDoubleValidator
from flow import Flow


class FlowInputContent(QDMNodeContentWidget):
    def initUI(self):
        # Create a QVBoxLayout to hold the widgets
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Add the first QLabel widget with the first description text
        description_label_fluid = QLabel("Enter fluid:")
        self.layout.addWidget(description_label_fluid)

        # @TODO implement dropdown with available fluids
        # Create the first QLineEdit widget with the default text "water"
        self.edit_fluid = QLineEdit("water", self)
        self.edit_fluid.setAlignment(Qt.AlignRight)
        self.edit_fluid.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_fluid)

        # Add the second QLabel widget with the second description text
        description_label_temp = QLabel("Enter temperature [K]:")
        self.layout.addWidget(description_label_temp)

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        # Create the second QLineEdit widget with an empty default text
        self.edit_temp = QLineEdit("293.15", self)
        self.edit_temp.setValidator(validator)
        self.edit_temp.setAlignment(Qt.AlignRight)
        self.edit_temp.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_temp)

        description_label_dm = QLabel("Enter mass flow rate [kg/s]:")
        self.layout.addWidget(description_label_dm)

        self.edit_mfr = QLineEdit("1", self)
        self.edit_mfr.setValidator(validator)
        self.edit_mfr.setAlignment(Qt.AlignRight)
        self.edit_mfr.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_mfr)

    def serialize(self):
        res = super().serialize()
        res['flow'] = self.node.flow.serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            flow = Flow.deserialize(data['flow'])
            self.edit_fluid.setText(flow.fluid)
            self.edit_temp.setText(str(flow.temperature))
            self.edit_mfr.setText(str(flow.mass_flow_rate))
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_INPUT)""
class NetworkNode_Input(FlowNode):
    op_code = OP_NODE_INPUT
    op_title = "Input Flow"
    content_label_objname = "flow_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = FlowInputContent(self)
        self.grNode = FlowGraphicsNode(self)

        self.content.edit_fluid.textChanged.connect(self.onInputChanged)
        self.content.edit_temp.textChanged.connect(self.onInputChanged)
        self.content.edit_mfr.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        fluid = self.content.edit_fluid.text()
        temp = float(self.content.edit_temp.text())
        mfr = float(self.content.edit_mfr.text())

        self.flow = Flow(fluid, temp, mfr)
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.flow
