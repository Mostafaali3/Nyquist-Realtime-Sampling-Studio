import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QVBoxLayout, QLineEdit, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from classes.viewer import Viewer
from classes.plotController import PlotController
from classes.signalComponent import SignalComponent
from helper_functions.component_generator import add_component, clear_layout
from helper_functions.signal_generator import add_signal
from helper_functions.component_generator import delete_component
from classes.mixer import Mixer



compile_qrc()

from icons_setup.compiledIcons import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Sampling Studio')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))

        self.components_grid_layout = self.componentsContainerWidget.layout()
        self.components_counter=1
        self.channles_counter = 1
        self.current_components=[]
        self.current_channles=[]
        self.current_shown_signal = None

        # self.components_layout = self.componentsContainerWidget.layout()

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

        self.signals_layout = self.signalsContainerWidget.layout()

        # add_signal(self.signals_layout, 1)
        # add_signal(self.signals_layout, 2)
        # add_signal(self.signals_layout, 3)
        # add_signal(self.signals_layout, 4)
        # add_signal(self.signals_layout, 5)
        # add_signal(self.signals_layout, 6)
        # add_signal(self.signals_layout, 7)



        #######
        # initializing the viewers
        self.sampling_viewer = Viewer()
        self.sampling_viewer.setBackground((30, 41, 59))
        self.sampling_viewer.getAxis('bottom').setPen('w')
        self.sampling_viewer.getAxis('left').setPen('w') 
        self.reconstruction_viewer = Viewer()
        self.reconstruction_viewer.setBackground((30, 41, 59))
        self.reconstruction_viewer.getAxis('bottom').setPen('w')
        self.reconstruction_viewer.getAxis('left').setPen('w') 
        self.error_viewer = Viewer()
        self.error_viewer.setBackground((30, 41, 59))
        self.error_viewer.getAxis('bottom').setPen('w')
        self.error_viewer.getAxis('left').setPen('w') 
        self.frequency_viewer = Viewer()
        self.frequency_viewer.setBackground((30, 41, 59))
        self.frequency_viewer.getAxis('bottom').setPen('w')
        self.frequency_viewer.getAxis('left').setPen('w') 
        
        self.controller = PlotController(self.sampling_viewer, self.reconstruction_viewer, self.error_viewer, self.frequency_viewer)
        # getting the viewrs frames 
        self.sampling_frame = self.findChild(QFrame, 'frame1')
        self.reconstruction_frame = self.findChild(QFrame, 'frame2')
        self.error_frame = self.findChild(QFrame, 'frame3')
        self.frequency_frame = self.findChild(QFrame, 'frame4')
        # intializing layouts 
        self.sampling_frame_layout = QVBoxLayout()
        self.reconstruction_frame_layout = QVBoxLayout()
        self.error_frame_layout = QVBoxLayout()
        self.frequency_frame_layout = QVBoxLayout()
        self.sampling_frame.setLayout(self.sampling_frame_layout)
        self.reconstruction_frame.setLayout(self.reconstruction_frame_layout)
        self.error_frame.setLayout(self.error_frame_layout)
        self.frequency_frame.setLayout(self.frequency_frame_layout)
        # appinding the frames 
        self.sampling_frame_layout.addWidget(self.sampling_viewer)
        self.reconstruction_frame_layout.addWidget(self.reconstruction_viewer)
        self.error_frame_layout.addWidget(self.error_viewer)
        self.frequency_frame_layout.addWidget(self.frequency_viewer)
        #######
        
        
        self.add_component_button = self.findChild(QPushButton,'addComponentButton')
        self.add_component_button.clicked.connect(self.add_component)
        
        self.add_signal_button = self.findChild(QPushButton,'addSignalButton')
        self.add_signal_button.clicked.connect(self.add_signal)
        
    def get_components_text(self):
        '''
        this function returns three floats that are written in the text lables 
        '''
        amplitude = float(self.findChild(QLineEdit, 'amplitudeInput').text())
        frequency = float(self.findChild(QLineEdit, 'frequencyInput').text())
        shift = float(self.findChild(QLineEdit, 'shiftInput').text())
        return amplitude, frequency, shift
        
    def add_component(self):
        amplitude, frequency, shift  = self.get_components_text()
        componenet = SignalComponent(amplitude, frequency, shift, self.components_counter)
        self.current_components.append(componenet)
        add_component(self.components_grid_layout,self.components_counter)
        component_delete_button = self.findChild(QPushButton, f'componentDeleteButton{self.components_counter}')
        component_delete_button.clicked.connect(lambda:self.delete_component(self.components_counter))
        self.components_counter+=1
        
    def delete_component(self, component_index): #loop on the signals and the elements and rearrange the indexing 
        self.current_components.pop(component_index-2)
        delete_component(self.components_grid_layout, component_index)
        
    def add_signal(self):
        mixer = Mixer()
        mixed_signal = mixer.mix_signal(self.current_components)
        mixed_signal.signal_id = self.channles_counter
        self.current_channles.append(mixed_signal)
        add_signal(self.signals_layout, self.channles_counter)
        self.current_shown_signal = mixed_signal
        self.controller.set_current_signal(self.current_shown_signal)
        self.current_components.clear()
        clear_layout(self.components_grid_layout)
        self.components_counter = 1
        self.channles_counter+=1
        
    def delete_signal(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())