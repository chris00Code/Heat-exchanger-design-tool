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
from PyQt5.QtGui import QDoubleValidator


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

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

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
        self.label_8.setValidator(validator)
        self.grid_layout.addWidget(self.label_8, 4, 1, 1, 1)

        label_9 = QLabel("k:")
        self.grid_layout.addWidget(label_9, 5, 0, 1, 1)
        self.label_10 = QLineEdit("", self)
        self.label_10.setValidator(validator)
        self.grid_layout.addWidget(self.label_10, 5, 1, 1, 1)

        label_11 = QLabel("A:")
        self.grid_layout.addWidget(label_11, 6, 0, 1, 1)
        self.label_12 = QLineEdit("", self)
        self.label_12.setValidator(validator)
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
        self.heat_capacity_flow = None
        # it's really important to mark all nodes Dirty by default
        self.markDirty()

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

        self.content.label_8.textChanged.connect(self.onCapFlowChanged)
        self.content.label_10.textChanged.connect(self.onkAChanged)
        self.content.label_12.textChanged.connect(self.onkAChanged)

    def onCapFlowChanged(self):
        print("%s::__onCapChanged" % self.__class__.__name__)
        l8 = self.content.label_8.text()
        l10 = self.content.label_10.text()
        l12 = self.content.label_12.text()
        if self.content.label_8.text() != '' \
                and self.content.label_10.text() == '' \
                and self.content.label_12.text() == '':
            self.content.label_10.setEnabled(False)
            self.content.label_12.setEnabled(False)
        else:
            self.content.label_10.setEnabled(True)
            self.content.label_12.setEnabled(True)
        self.markDirty()
        self.eval()

    def onkAChanged(self):
        print("%s::__onkAChanged" % self.__class__.__name__)
        if self.content.label_10.text() != '' or self.content.label_12.text() != '':
            self.content.label_8.setEnabled(False)
        else:
            self.content.label_8.setEnabled(True)
        self.markDirty()
        self.eval()
        if self.heat_capacity_flow is not None:
            self.content.label_8.setText(str(self.heat_capacity_flow))

    # @TODO change heatcapacity flow when changed to None
    def evalOperation(self):
        if self.content.label_10.text() != "" and self.content.label_12.text() != "":
            return float(self.content.label_10.text()) * float(self.content.label_12.text())
        elif self.content.label_8.text() != "":
            return float(self.content.label_8.text())
        else:
            return None

    # @TODO changing fluids when input changes
    def evalImplementation(self):
        input_1 = self.getInputWithSocketIndex(0)
        input_2 = self.getInputWithSocketIndex(1)

        # @TODO implement diversification of flows when same fluids
        if not any(item is None for item in input_1):
            self.out_flow_1 = input_1[0].get_flow(input_1[1])
            fluid_1 = self.out_flow_1.fluid
            self.content.label_3.setText(fluid_1)
        else:
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            self.content.label_3.setText("")
        if not any(item is None for item in input_2):
            self.out_flow_2 = input_2[0].get_flow(input_2[1])
            fluid_2 = self.out_flow_2.fluid
            self.content.label_5.setText(fluid_2)
        else:
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            self.content.label_5.setText("")
            return None
        if not any(item is None for item in zip(input_1, input_2)):
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
        self.heat_capacity_flow = self.evalOperation()
        if self.heat_capacity_flow is None:
            self.markDirty()
            self.markDescendantsDirty()
            dumpException("heat capacity flow not defined")

    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()

    # @TODO also serialize/deserialize k and A
    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        res['heat_capacity_flow'] = self.heat_capacity_flow
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.heat_capacity_flow = float(data['heat_capacity_flow'])
            self.content.label_8.setText(str(self.heat_capacity_flow))
        except Exception as e:
            dumpException(e)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res

    def get_flow(self, input):
        match input:
            case 0:
                return self.out_flow_1
            case 1:
                return self.out_flow_2
