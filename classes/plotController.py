from classes.viewer import Viewer
from classes.channel import Channel
from classes.signalReconstructor import signalReconstructor
import pyqtgraph as pg
class PlotController():
    def __init__(self, sampling_viewer:Viewer, reconstruction_viewer:Viewer, error_viewer:Viewer, frequency_viewer:Viewer,channels_dict:dict, current_channel:Channel = Channel()):
        self.sampling_viewer = sampling_viewer
        self.reconstruction_viewer = reconstruction_viewer
        self.error_viewer = error_viewer
        self.frequency_viewer = frequency_viewer
        self.__current_channel = current_channel
        self.current_channels_dict = channels_dict
        self.reconstructed_signal_obj = signalReconstructor([] , "Whittaker-Shannon" , 0 , [])
        
    @property
    def current_channel(self):
        return self.__current_channel    
    
    def plot(self):
        self.sampling_viewer.clear()
        if (len(self.current_channel.noise) != 0):
            self.sampling_viewer.plot(self.__current_channel.signal[0],self.__current_channel.signal[1] + self.current_channel.noise)
        else:
            self.sampling_viewer.plot(self.__current_channel.signal[0],self.__current_channel.signal[1])
        self.sampling_viewer.setLimits(xMin = 0,xMax =self.__current_channel.signal[0][-1])
        self.sampling_viewer.setXRange(0,self.__current_channel.signal[0][-1]/5)
        self.sampling_viewer.setYRange(min(self.__current_channel.signal[1]),max(self.__current_channel.signal[1]))
    
    def reconstruct_signal(self):
        self.reconstruction_viewer.clear()
        self.viewer_main_signal_x_values , viewer_main_signal_y_values = self.__current_channel.signal
        self.reconstructed_signal_obj.viewer_main_signal_max_frequency = self.__current_channel.max_frequency
        self.reconstructed_signal_obj.viewer_main_signal_time_points_array = self.viewer_main_signal_x_values
        if(len(self.current_channel.noise) != 0):
            self.reconstructed_signal_obj.viewer_main_signal = viewer_main_signal_y_values + self.current_channel.noise
        else:
            self.reconstructed_signal_obj.viewer_main_signal = viewer_main_signal_y_values
        reconstructed_signal_x_values , reconstructed_signal_y_values = self.reconstructed_signal_obj.reconstruct_main_viewer_signal()
        self.reconstruction_viewer.plot(reconstructed_signal_x_values , reconstructed_signal_y_values)
        self.reconstruction_viewer.setLimits(xMin = 0,xMax =self.__current_channel.signal[0][-1])
        self.reconstruction_viewer.setXRange(0,self.__current_channel.signal[0][-1]/5)
        self.reconstruction_viewer.setYRange(min(self.__current_channel.signal[1]),max(self.__current_channel.signal[1]))
        
    
    def reconstruction_error(self):
        self.error_viewer.clear()
        viewer_main_signal_reconstruction_error = self.reconstructed_signal_obj.calculate_reconstruction_error()
        self.error_viewer.plot(self.viewer_main_signal_x_values , viewer_main_signal_reconstruction_error)
        self.error_viewer.setLimits(xMin = 0,xMax =self.__current_channel.signal[0][-1])
        self.error_viewer.setXRange(0,self.__current_channel.signal[0][-1]/5)
        self.error_viewer.setYRange(min(self.__current_channel.signal[1]),max(self.__current_channel.signal[1]))
    
    def frequency_domain(self):
        self.frequency_viewer.clear()
        main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes = self.reconstructed_signal_obj.apply_fourier_transform_viewer_main_signal()
        self.frequency_viewer.plot(main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(0,255,0)))
        self.frequency_viewer.plot(-main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(0,255,0)))
        self.frequency_viewer.plot(-main_viewer_signal_frequencies + 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(255,0,0)))
        self.frequency_viewer.plot(main_viewer_signal_frequencies + 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(255,0,0)))
        self.frequency_viewer.plot(-main_viewer_signal_frequencies - 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(255,0,0)))
        self.frequency_viewer.plot(main_viewer_signal_frequencies - 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency , main_viewer_signal_fft_positive_magnitudes, pen=pg.mkPen(color=(255,0,0)))
        self.frequency_viewer.setLimits(xMin = -main_viewer_signal_frequencies[-1]- 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency,xMax =3000)
        print((main_viewer_signal_frequencies[-1] + 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency))
        self.frequency_viewer.setXRange(-main_viewer_signal_frequencies[-1] - 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency, -(-main_viewer_signal_frequencies[-1] - 2*self.reconstructed_signal_obj.signal_reconstruction_sampling_frequency))
        self.frequency_viewer.setYRange(min(main_viewer_signal_fft_positive_magnitudes),max(main_viewer_signal_fft_positive_magnitudes))
    
    def add_sample_points_on_viewer(self):
        sampled_time_values , sampled_signal_values = self.reconstructed_signal_obj.sample_viewer_main_signal()
        scatter_points_representing_samples = pg.ScatterPlotItem(pen=pg.mkPen('r'), brush=pg.mkBrush(255, 0, 0), size=10)
        scatter_points_representing_samples.setData(sampled_time_values, sampled_signal_values)
        self.sampling_viewer.addItem(scatter_points_representing_samples)
        
    def set_current_channel(self, new_signal:Channel):
        self.__current_channel = new_signal
        self.__current_channel.is_hidden = False
        for key, channel in self.current_channels_dict.items():
            if channel is not self.__current_channel:
                channel.is_hidden = True     
        self.plot()
        self.reconstruct_signal()
        self.reconstruction_error()
        self.frequency_domain()
        self.add_sample_points_on_viewer()
        
    