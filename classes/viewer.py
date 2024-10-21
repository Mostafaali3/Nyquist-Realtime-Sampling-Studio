import pyqtgraph as pg

class Viewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.__cgannels = []
        