from classes.viewer import Viewer
from classes.channel import Channel
class PlotController():
    def __init__(self, sampling_viewer:Viewer, reconstruction_viewer:Viewer, error_viewer:Viewer, frequency_viewer:Viewer,channels_dict:dict, current_channel:Channel = Channel()):
        self.sampling_viewer = sampling_viewer
        self.reconstruction_viewer = reconstruction_viewer
        self.error_viewer = error_viewer
        self.frequency_viewer = frequency_viewer
        self.__current_channel = current_channel
        self.current_channels_dict = channels_dict
        
        
    def plot(self):
        self.sampling_viewer.clear()
        self.sampling_viewer.plot(self.__current_channel.signal[0],self.__current_channel.signal[1])
        self.sampling_viewer.setLimits(xMin = 0,xMax =self.__current_channel.signal[0][-1])
        self.sampling_viewer.setXRange(0,self.__current_channel.signal[0][-1]/5)
        self.sampling_viewer.setYRange(min(self.__current_channel.signal[1]),max(self.__current_channel.signal[1]))
    
    def set_current_channel(self, new_signal:Channel):
        self.__current_channel = new_signal
        self.__current_channel.is_hidden = False
        for key, channel in self.current_channels_dict.items():
            if channel is not self.__current_channel:
                channel.is_hidden = True 
        self.plot()
        
    