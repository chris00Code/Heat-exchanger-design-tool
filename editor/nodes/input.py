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

        # Add a QLabel widget with the description text
        description_label = QLabel("Enter a value:")
        self.layout.addWidget(description_label)

        # Create a QLineEdit widget with the default text "1"
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit)
        """
        # Create a QLineEdit widget with the default text "1"
        self.edit = QLineEdit("1", self)
        # Set the alignment of the text in the QLineEdit widget to the right
        self.edit.setAlignment(Qt.AlignRight)
        # Set the object name of the widget to the value of self.node.content_label_objname
        self.edit.setObjectName(self.node.content_label_objname)
        """

    def serialize(self):
        # Serialize the data of the component
        res = super().serialize()
        # Add the text value of the QLineEdit widget to the serialized data
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        # Deserialize the data of the component
        res = super().deserialize(data, hashmap)
        try:
            # Try to retrieve the value from the data dictionary
            value = data['value']
            # Set the retrieved value as the text of the QLineEdit widget
            self.edit.setText(value)
            # Return True if the value was successfully set and deserialization was successful, otherwise False
            return True & res
        except Exception as e:
            # If an exception occurs, log the exception and return the result of deserialization
            dumpException(e)
        return res



"""
@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
"""


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
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
