import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from classes.channel import Channel
class signalReconstructor():
    def __init__(   
                    self , 
                    viewer_main_signal ,
                    selected_reconstruction_method,
                    viewer_main_signal_max_frequency,
                    viewer_main_signal_time_points_array,
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
        self.viewer_main_signal_time_points_array = viewer_main_signal_time_points_array
        
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
        if isinstance(new_viewer_main_signal , Channel) or isinstance(new_viewer_main_signal , list) or isinstance(new_viewer_main_signal , np.ndarray):
            self._viewer_main_signal= new_viewer_main_signal
    
    @signal_reconstruction_sampling_frequency.setter
    def signal_reconstruction_sampling_frequency(self , new_signal_reconstruction_sampling_frequency):
        if isinstance(new_signal_reconstruction_sampling_frequency , float) or isinstance(new_signal_reconstruction_sampling_frequency , int):
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
        if isinstance(new_reconstructed_signal , list) or isinstance(new_reconstructed_signal , np.ndarray):
            self._reconstructed_signal= new_reconstructed_signal
        
    @signal_reconstruction_error.setter
    def signal_reconstruction_error(self , new_signal_reconstruction_error):
        if isinstance(new_signal_reconstruction_error , list):
            self._signal_reconstruction_error= new_signal_reconstruction_error
    
    @viewer_main_signal_max_frequency.setter
    def viewer_main_signal_max_frequency(self , new_viewer_main_signal_max_frequency):
        if isinstance(new_viewer_main_signal_max_frequency , float) or isinstance(new_viewer_main_signal_max_frequency , int):
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

        if (self.selected_reconstruction_method == "Whittaker-Shannon" ):
            sampled_time_values , sampled_signal_values  = self.sample_viewer_main_signal() 
            self.reconstructed_signal = self.reconstruct_using_Whittaker_Shannon_formula(self.reconstuction_time_interval , sampled_signal_values )            
            # plt.plot(reconstuction_time_interval, self.reconstructed_signal)
            return self.reconstuction_time_interval , self.reconstructed_signal
        elif (self.selected_reconstruction_method == ""):
            pass
        
        elif(self.selected_reconstruction_method == ""):
            pass
    
    
    def reconstruct_using_Whittaker_Shannon_formula(self,reconstuction_time_interval, sampled_signal_values):
        reconstructed_signal = np.zeros_like(reconstuction_time_interval)
        for n, x_n in enumerate(sampled_signal_values):
            reconstructed_signal += x_n * np.sinc((reconstuction_time_interval - n /self.signal_reconstruction_sampling_frequency ) * self.signal_reconstruction_sampling_frequency)
        return reconstructed_signal
    
    
    def sample_viewer_main_signal(self):
        self.viewer_main_signal_time_points_length = len(self.viewer_main_signal_time_points_array)
        self.signal_reconstruction_max_sampling_frequency = 4 * self.viewer_main_signal_max_frequency
        self.reconstuction_time_interval = self.viewer_main_signal_time_points_array
        sampled_time_values = np.linspace(0 , int(round(self.viewer_main_signal_time_points_array[-1])) , (int(round(self.viewer_main_signal_time_points_array[-1]) * self.signal_reconstruction_sampling_frequency)) , endpoint= False )
        sampled_signal_values = np.interp(sampled_time_values, self.viewer_main_signal_time_points_array,  self.viewer_main_signal )
        # for single_signal_component in self.viewer_main_signal_components:
        #     sampled_signal_values += single_signal_component.amplitude * np.sin(2 * np.pi * sampled_time_values * single_signal_component.frequency)
        return sampled_time_values , sampled_signal_values
            
    def calculate_reconstruction_error(self):
        self.viewer_main_signal_reconstruction_error = self.viewer_main_signal - self.reconstructed_signal
        # plt.plot( self.viewer_main_signal_time_points_array, self.viewer_main_signal_reconstruction_error)
        # plt.show()
        return self.viewer_main_signal_reconstruction_error

    ################################
    # USING MATRIX DOT PRODUCT WAY #
    ################################
    # def reconstruct_using_Whittaker_Shannon_formula(self,reconstuction_time_interval, sampled_signal_values, sampled_time_values):
    #         sinc_matrix = np.sinc((reconstuction_time_interval[: , None] - sampled_time_values) * self.signal_reconstruction_sampling_frequency)
    #         return np.dot(sinc_matrix,sampled_signal_values)
    
    ####################################
    # OLD FUNCTION BEFORE KNOWING RFFT #
    ####################################    
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
    
    # def calculate_viewer_main_signal_max_frequency(self):
    #     if(self.is_loaded_signal):
    #         self.viewer_main_signal_sampling_rate = self.calcualte_loaded_signal_sample_rate()
    
    ##############################################
    # OLD FUNCTION BEFORE USING THE MAX FREQ WAY #
    ##############################################   
    #     main_viewer_signal_fft = np.fft.rfft(self.viewer_main_signal)
    #     main_viewer_signal_fft_positive_magnitudes = np.abs(main_viewer_signal_fft)
    #     # main_viewer_signal_frequencies = np.fft.rfftfreq(len(self.viewer_main_signal), self.viewer_main_signal_sampling_rate)
    #     # Replace up by down
    #     main_viewer_signal_frequencies = np.fft.rfftfreq(self.viewer_main_signal_time_points_length, 1/50)
    #     main_viewer_signal_max_frequency_index = np.argmax(main_viewer_signal_fft_positive_magnitudes)
    #     main_viewer_signal_max_frequency_value = main_viewer_signal_frequencies[main_viewer_signal_max_frequency_index]
    #     return main_viewer_signal_max_frequency_value
    
    def calculate_viewer_main_signal_max_frequency(self):
        if(self.is_loaded_signal):
            self.viewer_main_signal_sampling_rate = self.calcualte_loaded_signal_sample_rate()

        main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes = self.apply_fourier_transform_viewer_main_signal()
        plt.plot(main_viewer_signal_frequencies, main_viewer_signal_fft_positive_magnitudes)
        plt.show()
        nonzero_indices = np.where(main_viewer_signal_fft_positive_magnitudes > 200)[0]
        if nonzero_indices.size > 0:
            main_viewer_signal_max_frequency_value = main_viewer_signal_frequencies[nonzero_indices[-1]]
            return int(main_viewer_signal_max_frequency_value)
        else:
            return 0 
    
    def apply_fourier_transform_viewer_main_signal(self):
        main_viewer_signal_fft = np.fft.rfft(self.viewer_main_signal)
        main_viewer_signal_fft_positive_magnitudes = np.abs(main_viewer_signal_fft)
        main_viewer_signal_frequencies = np.fft.rfftfreq(self.viewer_main_signal_time_points_length, 1/50)
        
        return main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes
        
    def calcualte_loaded_signal_sample_rate(self):
        csv_signal = pd.read_csv('emg.csv')
        time_diffs_between_two_samples = csv_signal['time'].diff().dropna()
        csv_signal_delta_t = time_diffs_between_two_samples.mean()
        csv_signal_sample_rate = 1 / csv_signal_delta_t
        return csv_signal_sample_rate
########################################################################################################        
# def generate_continuous_signal(freq, duration, sampling_rate):
#         t = np.linspace(0, duration, int(sampling_rate * duration) , endpoint= False)
#         signal = np.sin(2 * np.pi * freq * t)
#         return signal ,t
# signal , t = generate_continuous_signal(freq= 4, duration=4 , sampling_rate=1000)

# def synthetic_mixed_signal():
#     component1 = SignalComponent(2.0 , 1.0 , 0.0 , 1)
#     component2 = SignalComponent(2.0 , 2.0 , 0.0 , 2)
#     component3 = SignalComponent(2.0 , 10.0 , 0.0 , 3)
#     component4 = SignalComponent(10.0 , 24.0 , 0.0 , 4)
#     component5 = SignalComponent(4.0 , 6.0 , 0.0 , 5)
#     components = {
#         'component1': component1,
#         'component2': component2,
#         'component3': component3,
#         'component4': component4,
#         'component5': component5
#     }
#     mixer = Mixer()
#     signal = mixer.mix_signal(components)
#     print(signal)
#     return signal.signal , signal.signal_components , signal.max_frequency

# t , signal , max_freq = synthetic_mixed_signal()
# plt.plot(t , signal)
# reconstruction = signalReconstructor(selected_reconstruction_method="Whittaker-Shannon" , viewer_main_signal=signal , viewer_main_signal_max_frequency= max_freq, viewer_main_signal_time_points_array= t)
# reconstruction.reconstruct_main_viewer_signal()
# reconstruction.calculate_reconstruction_error()
