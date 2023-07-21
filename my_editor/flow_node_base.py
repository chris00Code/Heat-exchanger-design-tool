from qtpy.QtGui import QImage, QPixmap
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel
from collections import OrderedDict
#from nodeeditor.node_node import Node
from new_node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException
from nodeeditor.node_serializable import Serializable
from flow import Flow
from graph_node import GraphNode

class FlowGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 200
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
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


class FlowContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class FlowNode(Node):
    icon = "icons/flow.png"
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = FlowGraphicsNode
    NodeContent_class = FlowContent

    def __init__(self, scene, inputs=[], outputs=[]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.flow = None

        self.graphNode = GraphNode(self.graph_node_title, self.id)
        # it's really important to mark all nodes Dirty by default
        self.markDirty()

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self, input1, input2):
        return 123

    def evalImplementation(self):
        pass

    def evalGraph(self):
        output_ids = self.getChildrenNodes()
        self.graphNode.output_ids = output_ids

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            #print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.flow

        try:
            self.evalGraph()
            flow = self.evalImplementation()
            return flow
        except NotImplementedError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()

    def serialize(self) -> OrderedDict:
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        ser_content = self.content.serialize() if isinstance(self.content, Serializable) else {}
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', ser_content),
        ])
        """
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res
        """

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res

    def get_flow(self, value=None):
        return self.flow
