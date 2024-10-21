import pyqtgraph as pg

class Viewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.__cgannels = []
        self.setLimits(xMin = 0, xMax = 1000)
        self.setBackground('w')
        self.showGrid(True, True)
        