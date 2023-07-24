# Import necessary modules from the qtpy library
from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

# Import modules from nodeeditor
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException

# Import custom modules from the project
from graph_node import GraphNode


# Custom class that extends QDMGraphicsNode to customize node appearance
class FlowGraphicsNode(QDMGraphicsNode):
    # Initialize default sizes and other parameters for the node
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 200
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    # Load custom icons for the node
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


# Custom class that extends QDMNodeContentWidget for displaying node content
class FlowContent(QDMNodeContentWidget):
    # Initialize the UI for the node content
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class FlowNode(Node):
    """
    Class representing 'Node' in the 'scence'
    contains relevant info of a Flow
    """

    GraphicsNode_class = FlowGraphicsNode
    NodeContent_class = FlowContent
    # @TODO may changing sockets fpr better usage
    # Socket_class = Socket

    icon = "icons/flow.png"
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    def __init__(self, scene, inputs=[], outputs=[]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.graphNode = GraphNode(self.graph_node_title, self.id)
        # it's really important to mark all nodes Dirty by default
        self.markDirty()

        self.flow = None
        # @TODO implement multi output
        self.output_ids = {"1": None}

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

        # @TODO may change to single edge and introduce mixers
        # self.output_multi_edged = True

    # node evaluations

    def evalImplementation(self):
        pass

    def eval(self):
        self.set_output_ids()
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.flow)
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

    # serialization functions

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        res['output_ids']= self.output_ids
        #res['children_ids'] = self.serialize_Children()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized FlowNode '%s'" % self.__class__.__name__, "res:", res)
        return res

    def serialize_Children(self):
        childrens = self.getChildrenNodes()
        ser_childs = []
        for child in childrens:
            ser_childs.append(child.id)
        return ser_childs

    def get_flow(self, value=None):
        return self.flow

    def evalGraph(self):
        output_ids = self.getChildrenNodes()
        self.graphNode.output_ids = output_ids

    def set_output_ids(self):
        try:
            outp_1 = self.getOutputs(0)[0].id
        except IndexError:
            outp_1 = None
        self.output_ids = {"1": outp_1}
