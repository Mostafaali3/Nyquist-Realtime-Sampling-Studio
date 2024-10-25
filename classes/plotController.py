from classes.viewer import Viewer
from classes.channel import Channel
class PlotController():
    def __init__(self, sampling_viewer:Viewer, reconstruction_viewer:Viewer, error_viewer:Viewer, frequency_viewer:Viewer, current_signal:Channel = Channel()):
        self.sampling_viewer = sampling_viewer
        self.reconstruction_viewer = reconstruction_viewer
        self.error_viewer = error_viewer
        self.frequency_viewer = frequency_viewer
        self.__current_signal = current_signal
        
        
    def plot(self):
        self.sampling_viewer.clear()
        self.sampling_viewer.plot(self.__current_signal.signal[0],self.__current_signal.signal[1])
        self.sampling_viewer.setLimits(xMin = 0,xMax =self.__current_signal.signal[0][-1])
        self.sampling_viewer.setXRange(0,self.__current_signal.signal[0][-1]/5)
        self.sampling_viewer.setYRange(min(self.__current_signal.signal[1]),max(self.__current_signal.signal[1]))
    
    def set_current_signal(self, new_signal:Channel):
        self.__current_signal = new_signal
        self.plot()
        
    