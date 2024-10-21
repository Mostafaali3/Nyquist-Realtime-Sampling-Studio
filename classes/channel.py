from PyQt5.QtWidgets import QFrame, QPushButton, QLineEdit, QHBoxLayout, QLabel

class Channel(QFrame):
    def __init__(self, signal:list = [], components:list = [], label:str = "unlinited", noise:list = []):
        super().__init__()
        self.__signal_components = components
        self.__label = label
        self.__signal = signal
        self.__noise = noise
        self.__status = "active" # active hidden or deleted 
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.show_hide_buttom = QPushButton("show/hide")
        self.delete_buttom = QPushButton("delete")
        self.signal_name = QLabel(self.__label)
        
        self.layout.addWidget(self.signal_name)
        self.layout.addWidget(self.delete_buttom)
        self.layout.addWidget(self.show_hide_buttom)
        
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
        
    
        
        