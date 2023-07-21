# from qtpy.QtWidgets import *
from qtpy.QtWidgets import *
from graph_editor_widget import GraphEditorWidget

class GraphEditorWindow(QMainWindow):
    GraphEditorWidget_class = GraphEditorWidget
    """Class representing GraphEditor's Main Window"""

    def __init__(self):
        """
        :Instance Attributes:

        - **name_company** - name of the company, used for permanent profile settings
        - **name_product** - name of this App, used for permanent profile settings
        """
        super().__init__()

        self.name_company = 'Lurger'
        self.name_product = 'GraphEditor'

        self.initUI()

    def initUI(self):
        # @TODO
        #  self.createActions()
        #  self.createMenus()

        # create graph editor widget
        self.grapheditor = self.__class__.GraphEditorWidget_class(self)
        #self.grapheditor.grScene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.grapheditor)

        #self.createStatusBar()

        # set window properties
        self.setTitle()
        self.show()

    def setTitle(self):
        """Function responsible for setting window title"""
        title = "Graph Editor"

        self.setWindowTitle(title)


"""
class GraphEditorWindow(QWidget):
    def __int__(self, parent= None):
        super().__int__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Editor")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # graphics view

        # window properties
        self.setGeometry(200, 200, 800, 600)

        self.show()
"""
