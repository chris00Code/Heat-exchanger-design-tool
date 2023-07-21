from qtpy.QtWidgets import *

from graph_graphics_scene import QDMGraphicsScene

class GraphEditorWidget(QWidget):
    #    Scene_class = Scene
    #    GraphicsView_class = QDMGraphicsView


    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.filename = None

        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,1800,600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.grScene = QDMGraphicsScene()

        # create graphics view
        self.view = QGraphicsView(self)
        self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)


