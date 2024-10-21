import numpy as np
from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QHBoxLayout, QLabel
class SignalComponent(QFrame):
    def __init__(self, amplitude:float, frequency:float, shift:float, func=np.sin):
        self.__amplitude = amplitude
        self.__frequency = frequency
        self.__shift = shift
        self.func = func 
        self.__label = f"amplitude:{self.__amplitude} freq: {self.__frequency} shift: {self.__shift}"
        self.__id = np.random.randint(100000, size=1)[0]
        
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.edit_buttom = QPushButton("edit")
        self.delete_buttom = QPushButton("delete")
        self.signal_name = QLabel(self.__label)
        
        self.layout.addWidget(self.signal_name)
        self.layout.addWidget(self.delete_buttom)
        self.layout.addWidget(self.edit_buttom)
        