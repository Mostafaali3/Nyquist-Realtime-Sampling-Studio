import numpy as np
from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QHBoxLayout, QLabel
class SignalComponent():
    def __init__(self, amplitude:float, frequency:float, shift:float, id:int,  func=np.sin):
        self.__amplitude = amplitude
        self.__frequency = frequency
        self.__shift = shift
        self.func = func 
        self.__label = f"amplitude:{self.__amplitude} freq: {self.__frequency} shift: {self.__shift}"
        self.__component_id = id
        
        # self.layout = QHBoxLayout()
        # self.setLayout(self.layout)
        
        # self.edit_buttom = QPushButton("edit")
        # self.delete_buttom = QPushButton("delete")
        # self.signal_name = QLabel(self.__label)
        
        # self.layout.addWidget(self.signal_name)
        # self.layout.addWidget(self.delete_buttom)
        # self.layout.addWidget(self.edit_buttom)
        
    @property
    def amplitude(self):
        return self.__amplitude
    
    @property
    def component_id(self):
        return self.__component_id
    
    @property
    def frequency(self):
        return self.__frequency
        
    @property
    def shift(self):
        return self.__shift
    
    @amplitude.setter
    def amplitude(self, new_amp):
        self.__amplitude = new_amp
        
    @frequency.setter
    def frequency(self, new_freq):
        self.__frequency = new_freq
        
    @shift.setter
    def shift(self, new_shift):
        self.__shift = new_shift