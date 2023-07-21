import os, sys
from qtpy.QtWidgets import *

#from graph_editor_wnd import GraphEditorWindow
from graph_editor_widget import GraphEditorWidget
if __name__ == '__main__':
    app = QApplication(sys.argv)

    #wnd = GraphEditorWindow()
    wnd = GraphEditorWidget()
    wnd.show()

    sys.exit(app.exec_())
