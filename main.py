import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QLabel,  QFrame, QVBoxLayout, QLineEdit, QWidget , QSlider, QCheckBox, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from classes.viewer import Viewer
from classes.plotController import PlotController
from classes.signalComponent import SignalComponent
from helper_functions.component_generator import add_component, clear_layout
from helper_functions.signal_generator import add_signal, delete_signal,show_hide_signal
from helper_functions.component_generator import delete_component
from classes.mixer import Mixer
from classes.signalReconstructor import signalReconstructor
from classes.noiser import Noiser
from classes.channel import Channel
from scipy.fft import fft, fftfreq
import numpy as np
from copy import copy, deepcopy
import math



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
        self.channels_counter = 1
        self.current_components= {}
        self.current_channles={}
        self.current_shown_channel = None

        # self.components_layout = self.componentsContainerWidget.layout()

        # add_component(self.components_grid_layout, 1)
        # add_component( self.components_grid_layout, 2)
        # add_component(self.components_grid_layout, 3)
        # add_component(self.components_grid_layout, 4)
        # add_component(self.components_grid_layout, 5)
        # add_component(self.components_grid_layout, 6)
        # add_component(self.components_grid_layout, 7)
        # add_component(self.components_grid_layout, 8)
        # add_component(self.components_grid_layout, 9)
        # add_component(self.components_grid_layout, 10)

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
        
        self.controller = PlotController(self.sampling_viewer, self.reconstruction_viewer, self.error_viewer, self.frequency_viewer,self.current_channles)
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
        
        # upload the signal
        self.upload_signal_button = self.findChild(QPushButton, 'uploadSignalButton')
        self.upload_signal_button.clicked.connect(self.upload_signal)
        
        
        # Initialize Nyquist Rate and Sampling Frequency Sliders
        self.nyquist_rate_slider = self.findChild(QSlider , "nequestRateSlider")
        self.nyquist_rate_slider.setMinimum(0)
        self.nyquist_rate_slider.setMaximum(4)
        self.nyquist_rate_slider.setPageStep(1)
        self.nyquist_slider_current_value_label = self.findChild(QLabel , "nequestRateValueLabel")
        self.nyquist_rate_slider.valueChanged.connect(self.nyquist_rate_slider_change_effect)
        
        self.sampling_frequency_slider = self.findChild(QSlider , "samplingFrequencySlider")
        self.sampling_frequency_slider.setMinimum(0)
        self.sampling_frequency_slider.setMaximum(1)
        self.sampling_frequency_slider.setPageStep(1)
        self.sampling_frequency_slider.valueChanged.connect(self.sampling_frequency_slider_change_effect)
        
        self.sampling_frequency_slider_current_value_label = self.findChild(QLabel , "samplingFrequencyValueLabel")
        self.sampling_frequency_max_value_label = self.findChild(QLabel , "label_22")
        self.sampling_frequency_max_value_label.setText("1")
        
        #Initialize Noise and SNR
        self.snr_value_label = self.findChild(QLabel , "SNRValueLabel")
        self.snr_value_label.setText("1")
        self.is_noise_added = self.findChild(QCheckBox , "noiseCheckBox")
        self.is_noise_added.stateChanged.connect(self.snr_checkbox_effect)
        
        self.snr_value_slider = self.findChild(QSlider , "noiseSlider")
        self.snr_value_slider.setMinimum(1)
        self.snr_value_slider.setMaximum(50)
        self.snr_value_slider.setPageStep(1)
        self.snr_value_slider.setValue(1)
        self.snr_value_slider.setDisabled(True)
        self.snr_value_slider.valueChanged.connect(self.snr_slider_effect)
        
        self.noiser_obj = Noiser()
        self.snr_value = 1
        
    def get_components_text(self):
        '''
        this function returns three floats that are written in the text lables 
        '''
        amplitude = float(self.findChild(QLineEdit, 'amplitudeInput').text())
        frequency = float(self.findChild(QLineEdit, 'frequencyInput').text())
        shift = float(self.findChild(QLineEdit, 'shiftInput').text())
        return amplitude, frequency, shift
        
    def add_component(self):
        if self.add_component_button.text() == 'Add Component':
            amplitude, frequency, shift  = self.get_components_text()
            componenet = SignalComponent(amplitude, frequency, shift, self.components_counter)
            self.current_components[self.components_counter] = componenet
            add_component(self.components_grid_layout,self.components_counter)
            component_label = self.findChild(QLabel, f"componentLabel{self.components_counter}")
            component_label.setText(componenet.label)
            component_delete_button = self.findChild(QPushButton, f'componentDeleteButton{self.components_counter}')
            current_component_index = copy(self.components_counter)
            component_delete_button.clicked.connect(lambda:self.delete_component(current_component_index))
            component_edit_button = self.findChild(QPushButton, f"componentEditButton{current_component_index}")
            component_edit_button.clicked.connect(lambda : self.edit_component_pressed(current_component_index))
            self.components_counter+=1
            
    def edit_component_pressed(self, component_index):
        component =  self.current_components[component_index]
        amplitude, frequency, shift =  component.amplitude, component.frequency, component.shift
        amplitude_textbox = self.findChild(QLineEdit, 'amplitudeInput')
        amplitude_textbox.setText(str(amplitude))
        frequency_textbox  = self.findChild(QLineEdit, 'frequencyInput')
        frequency_textbox.setText(str(frequency))
        shift_textbox  = self.findChild(QLineEdit, 'shiftInput')
        shift_textbox.setText(str(shift))
        self.add_component_button.setText("Edit Component")
        self.add_component_button.clicked.connect(lambda : self.edit_component(component_index))
    
    def edit_component(self, component_index):
        if self.add_component_button.text() == 'Edit Component':
            amplitude, frequency, shift = self.get_components_text()
            self.current_components[component_index].amplitude = amplitude
            self.current_components[component_index].frequency = frequency
            self.current_components[component_index].shift = shift
            component_label = self.findChild(QLabel, f"componentLabel{component_index}")
            component_label.setText(self.current_components[component_index].label)
            self.add_component_button.clicked.disconnect()
            self.add_component_button.setText("Add Component")
            self.add_component_button.clicked.connect(self.add_component)
        
        
    def delete_component(self, component_index): #loop on the signals and the elements and rearrange the indexing 
        self.current_components.pop(component_index)
        delete_component(self.components_grid_layout, component_index)
            
        
    def add_signal(self):
        mixer = Mixer()
        if len(self.current_components):
            mixed_channel = mixer.mix_signal(self.current_components)
            current_channel_index = copy(self.channels_counter)
            mixed_channel.signal_id = current_channel_index
            self.current_channles[current_channel_index] = mixed_channel
            add_signal(self.signals_layout, current_channel_index)
            self.current_shown_channel = mixed_channel
            self.controller.set_current_channel(self.current_shown_channel)
            self.set_sampling_frequency_slider_ranges()
            self.current_components.clear()
            clear_layout(self.components_grid_layout)
            self.components_counter = 1
            
            #activate the delete button
            signal_delete_button = self.findChild(QPushButton, f"signalDeleteButton{current_channel_index}")
            signal_delete_button.clicked.connect(lambda:self.delete_signal(current_channel_index))
            
            #activate the show hide button 
            show_hide_button = self.findChild(QPushButton, f"signalShowButton{current_channel_index}")
            show_hide_button.clicked.connect(lambda:self.show_signal(show_hide_button, current_channel_index))
            
            self.channels_counter+=1
        
    def delete_signal(self, current_index):
        self.current_channles.pop(current_index)#remove the signal from the dict 
        delete_signal(self.signals_layout, current_index)# remove the wodget of the signal
        
    def upload_signal(self):
        '''
        handles loading the signal
        '''
        file_path, _ = QFileDialog.getOpenFileName(self,'Open CSV File', '', 'CSV Files (*.csv);;All Files (*)' )
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
            data_x = (data['Time [s]'].iloc[0:1000]).to_numpy()
            data_y = (data[' II'].iloc[0:1000]).to_numpy()
            channel = Channel(signal_x=data_x, signal_y=data_y)
            channel.max_frequency = self.calculate_3db_frequency(channel)
            
            current_channel_index = copy(self.channels_counter)
            channel.signal_id = current_channel_index
            self.current_channles[current_channel_index] = channel

            add_signal(self.signals_layout, current_channel_index)
            self.current_shown_channel = channel
            self.controller.set_current_channel(self.current_shown_channel)
            self.set_sampling_frequency_slider_ranges()
            
            #activate the delete button
            signal_delete_button = self.findChild(QPushButton, f"signalDeleteButton{current_channel_index}")
            signal_delete_button.clicked.connect(lambda:self.delete_signal(current_channel_index))
            
            #activate the show hide button 
            show_hide_button = self.findChild(QPushButton, f"signalShowButton{current_channel_index}")
            show_hide_button.clicked.connect(lambda:self.show_signal(show_hide_button, current_channel_index))
            
            real_signal_label = self.findChild(QLabel, f"signalLabel{current_channel_index}")
            real_signal_label.setText(f"Loaded Signal {current_channel_index}")
            
            
            self.channels_counter+=1
        else:
            self.show_error("the file extention must be a csv file")
        
    def show_signal(self,current_button, current_index):
        self.current_shown_channel = self.current_channles[current_index]
        if self.current_shown_channel.is_hidden:
            self.current_shown_channel.is_hidden = False
            for key, channel in self.current_channles.items():
                if key !=current_index:
                    channel.is_hidden = True
            self.controller.set_current_channel(self.current_shown_channel)
            show_hide_signal(current_button, current_index)
            self.set_sampling_frequency_slider_ranges()
            
    def set_sampling_frequency_slider_ranges(self):
        self.sampling_frequency_slider.setMaximum(int(self.controller.current_channel.max_frequency) * 4)
        self.sampling_frequency_max_value_label.setText(str(int(self.controller.current_channel.max_frequency) * 4))

    def sampling_frequency_slider_change_effect(self , new_sampling_frequency):
        self.controller.reconstructed_signal_obj.signal_reconstruction_sampling_frequency = new_sampling_frequency
        self.sampling_frequency_slider_current_value_label.setText(str(new_sampling_frequency))
        self.controller.set_current_channel(self.current_shown_channel)
        self.nyquist_slider_current_value_label.setText(str(math.ceil(new_sampling_frequency * (1 / self.current_shown_channel.max_frequency))))
        self.nyquist_rate_slider.blockSignals(True)
        self.nyquist_rate_slider.setValue(math.ceil(new_sampling_frequency * (1/ self.current_shown_channel.max_frequency)))
        self.nyquist_rate_slider.blockSignals(False)
        
    def nyquist_rate_slider_change_effect(self , new_nyquist_rate):
        self.nyquist_slider_current_value_label.setText(str(new_nyquist_rate)) 
        self.controller.reconstructed_signal_obj.signal_reconstruction_sampling_frequency = int(new_nyquist_rate * self.current_shown_channel.max_frequency)
        self.sampling_frequency_slider_current_value_label.setText(str(int(new_nyquist_rate * self.current_shown_channel.max_frequency)))
        self.sampling_frequency_slider.blockSignals(True)
        self.sampling_frequency_slider.setValue(int(new_nyquist_rate * self.current_shown_channel.max_frequency))
        self.controller.set_current_channel(self.current_shown_channel)
        self.sampling_frequency_slider.blockSignals(False)

    def snr_checkbox_effect(self , current_state):
        if (current_state == 2):
            self.snr_value_slider.setEnabled(True)
            self.snr_value = self.snr_value_slider.value()
            generated_noise = self.noiser_obj.generate_noise(self.current_shown_channel , self.snr_value)
            self.current_shown_channel.noise = list(generated_noise)
        else:
            self.current_shown_channel.noise = []
            self.snr_value_slider.setDisabled(True)
        self.controller.set_current_channel(self.current_shown_channel)
    
    def snr_slider_effect(self , new_snr_value):
        self.snr_value_label.setText(str(new_snr_value))
        self.snr_value = new_snr_value
        if(self.is_noise_added.isChecked()):
            self.snr_checkbox_effect(2)
        else:
            self.snr_checkbox_effect(0)


    def calculate_3db_frequency(self,signal:Channel):
        time = np.array(signal.signal[0])
        readings = np.array(signal.signal[1])
        sampling_rate = 1 / (time[1] - time[0])

        # Perform FFT
        Y = np.fft.fft(readings)
        freqs = np.fft.fftfreq(len(readings), d=(time[1] - time[0]))

        # Calculate the magnitude spectrum
        magnitude = np.abs(Y)

        # Find the maximum magnitude and the corresponding 3dB level
        max_magnitude = np.max(magnitude)
        db_3_level = max_magnitude * 0.707
        
        index_3db = np.where(magnitude <= db_3_level)[0][0]
        frequency_3db = abs(freqs[index_3db])
        
        return db_3_level
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())