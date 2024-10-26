from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QHBoxLayout, QLabel
import numpy as np 
class Channel():
    def __init__(self,signal_x:list = [],  signal_y:list = [], components:list = [], label:bool = "unlinited", noise:list = []):
        self.__signal_components = components
        self.__label = label
        if not len(signal_x):
            signal_x = np.linspace(0,20,len(signal_y))
        self.__signal = [signal_x, signal_y]
        self.__noise = noise
        self.is_hidden = False # active hidden or deleted 
        self.signal_id = None
        
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
        
    
        
        