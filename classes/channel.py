from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QHBoxLayout, QLabel
import numpy as np 
import pandas as pd
class Channel():
    def __init__(self,signal_x:list = [],  signal_y:list = [], components:list = [], label:str = "unlinited", noise:list = [], max_frequency = None):
        self.__signal_components = components
        self.__label = label
        if not len(signal_x):
            signal_x = np.linspace(0,20,len(signal_y))
        self.__signal = [signal_x, signal_y]
        self.__noise = noise
        self.is_hidden = False # active hidden or deleted 
        self.signal_id = None
        self.max_frequency = max_frequency
        
        
    def export_to_csv(self):
        data_x = np.array(self.__signal[0])
        data_y = np.array(self.__signal[1])
        data = np.column_stack((data_x, data_y))
        data_frame = pd.DataFrame({"Time [s]":data_x, " II":data_y})
        data_frame.to_csv(f"signal_data_{self.signal_id}.csv", index=False)
    
    
    @property
    def signal(self):
        return self.__signal
    
    @property
    def label(self):
        return self.__label
        
    @property
    def signal_components(self):
        return self.__signal_components
    
    @property
    def noise(self):
        return self.__noise
    
    @label.setter
    def label(self, new_label):
        self.__label = new_label
    
    @noise.setter
    def noise(self, new_noise):
        self.__noise = new_noise
        
    
        
        