import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class signalReconstructor():
    def __init__(   
                    self , 
                    viewer_main_signal ,
                    selected_reconstruction_method,
                    viewer_main_signal_max_frequency,
                ):
        
        self._viewer_main_signal = viewer_main_signal
        self._signal_reconstruction_sampling_frequency = 0
        self._signal_reconstruction_nyquist_rate = 0
        self._selected_reconstruction_method = selected_reconstruction_method
        self.viewer_main_sampled_signal = []
        self._reconstructed_signal = []
        self._signal_reconstruction_error = [],
        self._viewer_main_signal_max_frequency = viewer_main_signal_max_frequency
        self._is_loaded_signal = False
        self._viewer_main_signal_sampling_rate = 1
        
    @property
    def viewer_main_signal(self):
        return self._viewer_main_signal
    
    @property
    def signal_reconstruction_sampling_frequency(self):
        return self._signal_reconstruction_sampling_frequency
    
    @property
    def signal_reconstruction_nyquist_rate(self):
        return self._signal_reconstruction_nyquist_rate
    
    @property
    def selected_reconstruction_method(self):
        return self._selected_reconstruction_method
    
    @property
    def sampled_signal(self):
        return self.viewer_main_sampled_signal
    
    @property
    def reconstructed_signal(self):
        return self._reconstructed_signal
    
    @property
    def signal_reconstruction_error(self):
        return self._signal_reconstruction_error
    
    @property
    def viewer_main_signal_max_frequency(self):
        return self._viewer_main_signal_max_frequency
    
    @property
    def is_loaded_signal(self):
        return self._is_loaded_signal
    
    @property
    def viewer_main_signal_sampling_rate(self):
        return self._viewer_main_signal_sampling_rate
    
    @viewer_main_signal.setter
    def viewer_main_signal(self , new_viewer_main_signal):
        if isinstance(new_viewer_main_signal , channel):
            self._viewer_main_signal= new_viewer_main_signal
    
    @signal_reconstruction_sampling_frequency.setter
    def signal_reconstruction_sampling_frequency(self , new_signal_reconstruction_sampling_frequency):
        if isinstance(new_signal_reconstruction_sampling_frequency , float):
            self._signal_reconstruction_sampling_frequency= new_signal_reconstruction_sampling_frequency
    
    @signal_reconstruction_nyquist_rate.setter
    def signal_reconstruction_nyquist_rate(self , new_signal_reconstruction_nyquist_rate):
        if isinstance(new_signal_reconstruction_nyquist_rate , float):
            self._signal_reconstruction_nyquist_rate= new_signal_reconstruction_nyquist_rate
        
    @selected_reconstruction_method.setter
    def selected_reconstruction_method(self , new_selected_reconstruction_method):
        if isinstance(new_selected_reconstruction_method , str):
            self._selected_reconstruction_method= new_selected_reconstruction_method
        
    @sampled_signal.setter
    def sampled_signal(self , newviewer_main_sampled_signal):
        if isinstance(newviewer_main_sampled_signal , list):
            self.viewer_main_sampled_signal= newviewer_main_sampled_signal
        
    @reconstructed_signal.setter
    def reconstructed_signal(self , new_reconstructed_signal):
        if isinstance(new_reconstructed_signal , list):
            self._reconstructed_signal= new_reconstructed_signal
        
    @signal_reconstruction_error.setter
    def signal_reconstruction_error(self , new_signal_reconstruction_error):
        if isinstance(new_signal_reconstruction_error , list):
            self._signal_reconstruction_error= new_signal_reconstruction_error
    
    @viewer_main_signal_max_frequency.setter
    def viewer_main_signal_max_frequency(self , new_viewer_main_signal_max_frequency):
        if isinstance(new_viewer_main_signal_max_frequency , float):
            self._viewer_main_signal_max_frequency= new_viewer_main_signal_max_frequency
    
    @is_loaded_signal.setter
    def is_loaded_signal(self , new_loaded_signal):
        if isinstance(new_loaded_signal , bool):
            self._is_loaded_signal= new_loaded_signal
            
    @viewer_main_signal_sampling_rate.setter
    def viewer_main_signal_sampling_rate(self , new_viewer_main_signal_sampling_rate):
        if isinstance(new_viewer_main_signal_sampling_rate , float):
            self._viewer_main_signal_sampling_rate= new_viewer_main_signal_sampling_rate
            
    def reconstruct_main_viewer_signal(self):
        if (self.selected_reconstruction_method == "Nyquist-Shannon" ):
            self.viewer_main_signal_time_points = len(self.viewer_main_signal)
            self.viewer_main_signal_max_frequency = self.calculate_viewer_main_signal_max_frequency()
            self.signal_reconstruction_max_sampling_frequency = 4 * self.viewer_main_signal_max_frequency
            self.viewer_main_signal_sampling_rate = 9
            sampling_time_interval = np.arange(0 , self.viewer_main_signal_time_points , 1 / self.viewer_main_signal_sampling_rate)
            self.viewer_main_sampled_signal = np.sin(2 * np.pi * 9 * sampling_time_interval)
            plt.plot(sampling_time_interval, self.viewer_main_sampled_signal)
            plt.show()
        elif (self.selected_reconstruction_method == ""):
            pass
        
        elif(self.selected_reconstruction_method == ""):
            pass
    
    # OLD FUNCTION BEFORE KNOWING RFFT    
    # def calculate_viewer_main_signal_max_frequency(self):
    #     if(self.is_loaded_signal):
    #         self.viewer_main_signal_sampling_rate = self.calcualte_loaded_signal_sample_rate()

        
    #     main_viewer_signal_fft = np.fft.fft(self.viewer_main_signal)
    #     main_viewer_signal_fft_positive_magnitudes = np.abs(main_viewer_signal_fft[:self.viewer_main_signal_time_points//2])
    #     # main_viewer_signal_frequencies = np.fft.fftfreq(len(self.viewer_main_signal), self.viewer_main_signal_sampling_rate)
    #     # Replace up by down
    #     main_viewer_signal_frequencies = np.fft.fftfreq(self.viewer_main_signal_time_points, 1/9)
    #     main_viewer_signal_positive_frequencies = main_viewer_signal_frequencies[:self.viewer_main_signal_time_points//2]
        
    #     main_viewer_signal_max_frequency_index = np.argmax(main_viewer_signal_fft_positive_magnitudes)
    #     main_viewer_signal_max_frequency_value = main_viewer_signal_positive_frequencies[main_viewer_signal_max_frequency_index]
        
    #     return main_viewer_signal_max_frequency_value
    
    def calculate_viewer_main_signal_max_frequency(self):
        if(self.is_loaded_signal):
            self.viewer_main_signal_sampling_rate = self.calcualte_loaded_signal_sample_rate()

        
        main_viewer_signal_fft = np.fft.rfft(self.viewer_main_signal)
        main_viewer_signal_fft_positive_magnitudes = np.abs(main_viewer_signal_fft)
        # main_viewer_signal_frequencies = np.fft.fftfreq(len(self.viewer_main_signal), self.viewer_main_signal_sampling_rate)
        # Replace up by down
        main_viewer_signal_frequencies = np.fft.rfftfreq(self.viewer_main_signal_time_points, 1/9)
        
        main_viewer_signal_max_frequency_index = np.argmax(main_viewer_signal_fft_positive_magnitudes)
        main_viewer_signal_max_frequency_value = main_viewer_signal_frequencies[main_viewer_signal_max_frequency_index]
        
        return main_viewer_signal_max_frequency_value
    
    def calcualte_loaded_signal_sample_rate(self):
        csv_signal = pd.read_csv('emg.csv')
        time_diffs_between_two_samples = csv_signal['time'].diff().dropna()
        csv_signal_delta_t = time_diffs_between_two_samples.mean()
        csv_signal_sample_rate = 1 / csv_signal_delta_t
        return csv_signal_sample_rate
        
def generate_continuous_signal(freq, duration, sampling_rate):
        t = np.linspace(0, duration, int(sampling_rate * duration))
        signal = np.sin(2 * np.pi * freq * t)
        return signal
    
signal = generate_continuous_signal(freq= 4, duration=4 , sampling_rate=9)
signalReconstructor(selected_reconstruction_method="Nyquist-Shannon" , viewer_main_signal=signal , viewer_main_signal_max_frequency= 0).reconstruct_main_viewer_signal()