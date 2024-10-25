from classes.viewer import Viewer
from classes.channel import Channel
class PlotControler():
    def __init__(self, sampling_viewer:Viewer, reconstruction_viewer:Viewer, error_viewer:Viewer, frequency_viewer:Viewer, current_signal:Channel):
        self.sampling_viewer = sampling_viewer
        self.reconstruction_viewer = reconstruction_viewer
        self.error_viewer = error_viewer
        self.frequency_viewer = frequency_viewer
        self.current_signal = current_signal
        
        
    def plot(self):
        self.sampling_viewer.clear()
        self.sampling_viewer.plotItem(self.current_signal.signal)
        
    