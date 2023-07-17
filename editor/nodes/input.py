from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from calc_conf import register_node, OP_NODE_INPUT
from calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from PyQt5.QtWidgets import QVBoxLayout, QLabel


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        # Create a QVBoxLayout to hold the widgets
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Add the first QLabel widget with the first description text
        description_label_fluid = QLabel("Enter fluid:")
        self.layout.addWidget(description_label_fluid)

        #@TODO implement dropdown with available fluids
        # Create the first QLineEdit widget with the default text "water"
        self.edit_fluid = QLineEdit("water", self)
        self.edit_fluid.setAlignment(Qt.AlignRight)
        self.edit_fluid.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_fluid)

        # Add the second QLabel widget with the second description text
        description_label_temp = QLabel("Enter temperature [K]:")
        self.layout.addWidget(description_label_temp)

        # Create the second QLineEdit widget with an empty default text
        self.edit_temp = QLineEdit("293.15", self)
        self.edit_temp.setAlignment(Qt.AlignRight)
        self.edit_temp.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_temp)


        description_label_dm = QLabel("Enter mass flow rate [kg/s]:")
        self.layout.addWidget(description_label_dm)

        self.edit_dm = QLineEdit("1", self)
        self.edit_dm.setAlignment(Qt.AlignRight)
        self.edit_dm.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit_dm)

    def serialize(self):
        res = super().serialize()
        res['fluid'] = self.edit_fluid.text()
        res['temperature'] = self.edit_temp.text()
        res['mass flow rate'] = self.edit_dm.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value1 = data['fluid']
            value2 = data['temperature']
            value3 = data['mass flow rate']
            self.edit_fluid.setText(value1)
            self.edit_temp.setText(value2)
            self.edit_dm.setText(value3)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_INPUT)
class NetworkNode_Input(CalcNode):
    icon = "icons/flow.png"
    op_code = OP_NODE_INPUT
    op_title = "Input Flow"
    content_label_objname = "network_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height = 160

        self.content.edit_fluid.textChanged.connect(self.onInputChanged)
        self.content.edit_temp.textChanged.connect(self.onInputChanged)
        self.content.edit_dm.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        fluid = self.content.edit_fluid.text()
        temp = self.content.edit_temp.text()
        dm = self.content.edit_dm.text()

        #@TODO eval of parameters
        self.value = None
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
