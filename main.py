import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from helper_functions.component_generator import add_component
from helper_functions.component_generator import delete_component


compile_qrc()

from icons_setup.compiledIcons import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Sampling Studio')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))

        self.grid_layout = self.componentsContainerWidget.layout()

        # add_component(self.grid_layout, 1)
        # add_component( self.grid_layout, 2)
        # add_component(self.grid_layout, 3)
        # add_component(self.grid_layout, 4)
        # add_component(self.grid_layout, 5)
        # add_component(self.grid_layout, 6)
        # add_component(self.grid_layout, 7)
        # add_component(self.grid_layout, 8)
        # add_component(self.grid_layout, 9)
        # add_component(self.grid_layout, 10)

        # self.componentDeleteButton1 = self.findChild(QPushButton, "componentDeleteButton1")
        # self.componentDeleteButton1.clicked.connect(lambda: delete_component(self.grid_layout, 1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())