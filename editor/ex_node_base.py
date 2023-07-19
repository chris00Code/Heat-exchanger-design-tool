from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException
from PyQt5 import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qtpy.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit
from flow import Flow


class ExGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 170
        self.height = 200
        self.edge_roundness = 6
        self.edge_padding = 5
        self.title_horizontal_padding = 15
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )

        image_path = self.node.icon
        image = QImage(image_path)
        painter.drawImage(QRectF(100, 0, 24.0, 24.0), image)


class ExContent(QDMNodeContentWidget):
    def initUI(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid_layout)

        font1 = QtGui.QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setWeight(75)

        label_1 = QLabel("Input fluids:")
        label_1.setFont(font1)
        self.grid_layout.addWidget(label_1, 0, 0, 1, 2)

        label_2 = QLabel("fluid 1:")
        self.grid_layout.addWidget(label_2, 1, 0, 1, 1)

        self.label_3 = QLabel("", self)
        self.label_3.setObjectName(self.node.content_label_objname)
        self.grid_layout.addWidget(self.label_3, 1, 1, 1, 1)

        label_4 = QLabel("fluid 2:")
        self.grid_layout.addWidget(label_4, 2, 0, 1, 1)

        self.label_5 = QLabel("", self)
        self.label_5.setObjectName(self.node.content_label_objname)
        self.grid_layout.addWidget(self.label_5, 2, 1, 1, 1)

        label_6 = QLabel("Parameters:")
        label_6.setFont(font1)
        self.grid_layout.addWidget(label_6, 3, 0, 1, 2)

        label_7 = QLabel("heat capacity flow:")
        self.grid_layout.addWidget(label_7, 4, 0, 1, 1)
        self.label_8 = QLineEdit("", self)
        self.grid_layout.addWidget(self.label_8, 4, 1, 1, 1)

        label_9 = QLabel("k:")
        self.grid_layout.addWidget(label_9, 5, 0, 1, 1)
        self.label_10 = QLineEdit("", self)
        self.grid_layout.addWidget(self.label_10, 5, 1, 1, 1)

        label_11 = QLabel("A:")
        self.grid_layout.addWidget(label_11, 6, 0, 1, 1)
        self.label_12 = QLineEdit("", self)
        self.grid_layout.addWidget(self.label_12, 6, 1, 1, 1)


class ExNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "excalc_node_bg"

    GraphicsNode_class = ExGraphicsNode
    NodeContent_class = ExContent

    def __init__(self, scene, inputs=[2, 2], outputs=[2, 2]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.out_flow_1 = None
        self.out_flow_2 = None
        # it's really important to mark all nodes Dirty by default
        self.markDirty()

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self, input1, input2):
        raise NotImplementedError

    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        # @TODO implement diversification of flows when same fluids
        if i1 is not None:
            self.out_flow_1 = i1
            fluid_1 = i1.content.edit_fluid.text()
            self.content.label_3.setText(fluid_1)
        if i2 is not None:
            self.out_flow_2 = i2
            fluid_2 = i2.content.edit_fluid.text()
            self.content.label_5.setText(fluid_2)
        if i1 and i2 is None:
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None
        else:
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__)
            return None

        try:
            self.evalImplementation()
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)
        """
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)
        """

    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
