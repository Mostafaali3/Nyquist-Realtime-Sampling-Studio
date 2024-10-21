import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QScrollBar, QFrame, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
import pyqtgraph as pg
import pandas as pd
from classes.viewer import Viewer
from classes.channel import Channel
from classes.signalComponent import SignalComponent

class MixerTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        
        self.viewers_widget = QWidget()
        self.mixer_widget = QWidget()
        
        self.layout.addWidget(self.viewers_widget)
        self.layout.addWidget(self.mixer_widget)
        
        self.mixer_layout = QVBoxLayout()
        self.viewers_layout = QVBoxLayout()
        
        self.viewers_widget.setLayout(self.viewers_layout)
        self.mixer_widget.setLayout(self.mixer_layout)
        
        self.mixed_signal_plot_widget = Viewer()
        self.reconstructed_signal_plot_widget = Viewer()
        
        self.viewers_layout.addWidget(self.mixed_signal_plot_widget)
        self.viewers_layout.addWidget(self.reconstructed_signal_plot_widget)
        
        ## adding signals frame
        self.make_signal_frame = QFrame()
        self.make_signal_layout = QVBoxLayout()
        self.make_signal_frame.setLayout(self.make_signal_layout)
        
        self.frequency_text = QLineEdit(QIntValidator(0, 9999, self))
        self.amplitude_text = QLineEdit(QIntValidator(0, 9999, self))
        self.shift_text = QLineEdit(QIntValidator(0, 9999, self))
        self.add_signal_button = QPushButton("ADD SIGNAL")
        
        self.make_signal_layout.addWidget(self.amplitude_text)
        self.make_signal_layout.addWidget(self.frequency_text)
        self.make_signal_layout.addWidget(self.shift_text)
        self.make_signal_layout.addWidget(self.add_signal_button)
        
        self.mixer_layout.addWidget(self.make_signal_frame)
        
        self.components_frame = QFrame()
        self.components_frame_layout = QVBoxLayout()
        self.components_frame.setLayout(self.components_frame_layout)
        
        self.mixer_layout.addWidget(self.components_frame)
        
        
        for i in range(3):
            self.test_signal = Channel(label="test signal")
            self.mixer_layout.addWidget(self.test_signal)
            
    def add_signal_component(self):
        frequency = int(self.frequency_text.text())
        amplitude = int(self.frequency_text.text())
        shift  = int(self.frequency_text.text())
        
def main():
    app = QApplication(sys.argv)
    window = MixerTestWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
        