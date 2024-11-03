import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from classes.channel import Channel
import pywt
from scipy.interpolate import interp1d


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
        sampled_time_values , sampled_signal_values  = self.sample_viewer_main_signal() 
        if (self.selected_reconstruction_method == "Whittaker Shannon" ):
            self.reconstructed_signal = self.reconstruct_using_Whittaker_Shannon_formula(self.reconstuction_time_interval , sampled_signal_values )            
            # plt.plot(reconstuction_time_interval, self.reconstructed_signal)        
        elif self.selected_reconstruction_method == "Hann":
            self.reconstructed_signal = self.reconstruct_using_hann(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        elif self.selected_reconstruction_method == "Hamming":
            self.reconstructed_signal = self.reconstruct_using_hamming(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        elif self.selected_reconstruction_method == "Zero Hold":
            self.reconstructed_signal = self.reconstruct_using_zero_hold(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        elif self.selected_reconstruction_method == "First Order":
            self.reconstructed_signal = self.reconstruct_using_first_order_hold(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        elif self.selected_reconstruction_method == "Kaiser":
            self.reconstructed_signal = self.reconstruct_using_kaiser(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        elif (self.selected_reconstruction_method == "Lanczos"):
            self.reconstructed_signal = self.reconstruct_using_lanczos(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        elif (self.selected_reconstruction_method == "sinc_kaiser"):
            self.reconstructed_signal = self.reconstruct_using_lanczos(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        
        elif(self.selected_reconstruction_method == "Deponacchi"):
            self.reconstructed_signal = self.reconstruct_using_wavelet(
                self.viewer_main_signal_time_points_array, sampled_signal_values
            )
        
        return self.reconstuction_time_interval , self.reconstructed_signal
    
    def reconstruct_using_Whittaker_Shannon_formula(self,reconstuction_time_interval, sampled_signal_values):
        reconstructed_signal = np.zeros_like(reconstuction_time_interval)
        for n, x_n in enumerate(sampled_signal_values):
            reconstructed_signal += x_n * np.sinc((reconstuction_time_interval - n /self.signal_reconstruction_sampling_frequency ) * self.signal_reconstruction_sampling_frequency)
        return reconstructed_signal
    
    def reconstruct_using_zero_hold(self, reconstruction_time_interval, sampled_signal_values):
        """
        Zero-order hold reconstruction method.
        """
        reconstructed_signal = np.zeros_like(reconstruction_time_interval)
        if self.signal_reconstruction_sampling_frequency == 0:
            sampling_period = 1 / (self.signal_reconstruction_sampling_frequency+1)
        else:
            sampling_period = 1 / self.signal_reconstruction_sampling_frequency
            
        for n, x_n in enumerate(sampled_signal_values):
            start_time = n * sampling_period
            end_time = (n + 1) * sampling_period
            hold_indices = np.where((reconstruction_time_interval >= start_time) & 
                                    (reconstruction_time_interval < end_time))
            
            reconstructed_signal[hold_indices] = x_n
        
        return reconstructed_signal

    def reconstruct_using_first_order_hold(self, reconstruction_time_interval, sampled_signal_values):
        """
        First-order hold (linear interpolation) reconstruction method with edge case handling.
        """
        if len(sampled_signal_values) == 0:
            return np.zeros_like(reconstruction_time_interval)
        
        reconstructed_signal = np.zeros_like(reconstruction_time_interval)
        
        sampling_period = 1 / self.signal_reconstruction_sampling_frequency if self.signal_reconstruction_sampling_frequency > 0 else 1.0
        
        for n in range(len(sampled_signal_values) - 1):
            x_n = sampled_signal_values[n]
            x_next = sampled_signal_values[n + 1]
            
            start_time = n * sampling_period
            end_time = (n + 1) * sampling_period
            
            interval_indices = np.where((reconstruction_time_interval >= start_time) &
                                        (reconstruction_time_interval < end_time))
            
            t = (reconstruction_time_interval[interval_indices] - start_time) / (end_time - start_time)
            reconstructed_signal[interval_indices] = x_n * (1 - t) + x_next * t
        
        if len(sampled_signal_values) > 1:
            reconstructed_signal[reconstruction_time_interval >= (len(sampled_signal_values) - 1) * sampling_period] = sampled_signal_values[-1]
        else:
            reconstructed_signal[:] = sampled_signal_values[0]
        
        return reconstructed_signal


    def reconstruct_using_hann(self, reconstuction_time_interval, sampled_signal_values):
        reconstructed_signal = np.zeros_like(reconstuction_time_interval)
        signal_fft = np.fft.fft(sampled_signal_values)

        N = len(reconstuction_time_interval)
        hamming_window = np.hamming(N)
        windowed_fft = signal_fft * hamming_window  # Element-wise multiplication
        reconstructed_signal = np.fft.ifft(windowed_fft)
        return reconstructed_signal
    
    def reconstruct_using_hamming(self, reconstruction_time, sampled_signal_values):
        reconstructed_signal = np.zeros_like(reconstruction_time)
        sampling_period = 1 / self.signal_reconstruction_sampling_frequency if self.signal_reconstruction_sampling_frequency > 0 else 1.0
        N = len(sampled_signal_values)
        
        for n, x_n in enumerate(sampled_signal_values):
            window_size = max(3, N - abs(n - (N // 2)))
            hamming_window = np.hamming(window_size)
            center_time = n * sampling_period
            window_times = np.linspace(-0.5, 0.5, window_size) * window_size / self.signal_reconstruction_sampling_frequency
            
            # Convolve the sample with the Hamming window over valid intervals
            convolution = x_n * hamming_window
            for i, t_shift in enumerate(window_times):
                interval_indices = np.where(
                    (reconstruction_time >= center_time + t_shift - sampling_period / 2) &
                    (reconstruction_time < center_time + t_shift + sampling_period / 2)
                )[0]
                
                if interval_indices.size > 0:
                    reconstructed_signal[interval_indices] += convolution[i]
        
        return reconstructed_signal
        
    def reconstruct_using_kaiser(self, reconstruction_time, sampled_signal_values, beta=8.6):
        reconstructed_signal = np.zeros_like(reconstruction_time)
        sampling_period = 1 / self.signal_reconstruction_sampling_frequency if self.signal_reconstruction_sampling_frequency > 0 else 1.0
        N = len(sampled_signal_values)
        
        for n, x_n in enumerate(sampled_signal_values):
            window_size = max(3, N - abs(n - (N // 2)))
            kaiser_window = np.kaiser(window_size,8.6)
            center_time = n * sampling_period
            window_times = np.linspace(-0.5, 0.5, window_size) * window_size / self.signal_reconstruction_sampling_frequency
            convolution = x_n * kaiser_window
            for i, t_shift in enumerate(window_times):
                interval_indices = np.where(
                    (reconstruction_time >= center_time + t_shift - sampling_period / 2) &
                    (reconstruction_time < center_time + t_shift + sampling_period / 2)
                )[0]
                
                if interval_indices.size > 0:
                    reconstructed_signal[interval_indices] += convolution[i]
        
        return reconstructed_signal


    def reconstruct_using_sinc_kaiser(self, reconstruction_time, sampled_signal_values, beta=8.6):
        reconstructed_signal = np.zeros_like(reconstruction_time)
        sampling_period = 1 / self.signal_reconstruction_sampling_frequency if self.signal_reconstruction_sampling_frequency > 0 else 1.0
        N = len(sampled_signal_values)
        kaiser_window = np.kaiser(N, beta)
        
        for n, x_n in enumerate(sampled_signal_values):
            time_diff = reconstruction_time - n * sampling_period
            sinc_kaiser = np.sinc(time_diff / sampling_period) * kaiser_window[n]
            reconstructed_signal += x_n * sinc_kaiser
        return reconstructed_signal

        
    def reconstruct_using_lanczos(self,reconstuction_time_interval, sampled_signal_values):
        reconstructed_signal = np.zeros_like(reconstuction_time_interval)
        for n, x_n in enumerate(sampled_signal_values):
            time_diff = (reconstuction_time_interval - n / self.signal_reconstruction_sampling_frequency) if self.signal_reconstruction_sampling_frequency > 0 else (reconstuction_time_interval - n)  # Handle division by zero
            sinc_term = np.sinc(time_diff * self.signal_reconstruction_sampling_frequency)
            lanczos_window = np.sinc(time_diff / 3)
            reconstructed_signal += x_n * sinc_term * lanczos_window
        return reconstructed_signal
    
    
    def reconstruct_using_wavelet(self, reconstuction_time_interval, sampled_signal_values, wavelet='db1'):

        coeffs = pywt.wavedec(sampled_signal_values, wavelet)
        reconstructed_signal = pywt.waverec(coeffs, wavelet)
        time_scale_factor = reconstuction_time_interval[-1] / len(reconstructed_signal)
        reconstructed_signal = np.interp(
            reconstuction_time_interval,  # target interval (e.g., 0 to 20)
            np.linspace(0, reconstuction_time_interval[-1], len(reconstructed_signal)),  # reconstructed interval
            reconstructed_signal
        )
        
        return reconstructed_signal
    
    
    def sample_viewer_main_signal(self):
        self.viewer_main_signal_time_points_length = len(self.viewer_main_signal_time_points_array)
        self.signal_reconstruction_max_sampling_frequency = 4 * self.viewer_main_signal_max_frequency
        self.reconstuction_time_interval = self.viewer_main_signal_time_points_array
        sampled_time_values = np.linspace(0 , int(round(self.viewer_main_signal_time_points_array[-1])) , (int(round(self.viewer_main_signal_time_points_array[-1]) * self.signal_reconstruction_sampling_frequency)) , endpoint= False )
        sampled_signal_values = np.interp(sampled_time_values, self.viewer_main_signal_time_points_array,  self.viewer_main_signal )
        # interpolator = interp1d(self.viewer_main_signal_time_points_array, self.viewer_main_signal, kind='cubic')
        # sampled_signal_values = interpolator(sampled_time_values)
        # self.reconstuction_time_interval = list(self.reconstuction_time_interval)
        # self.viewer_main_signal = list(self.viewer_main_signal)
        # if (len(sampled_signal_values) != 0 and len(sampled_signal_values) < 1000):
        #     temp_viewer_main_signal = self.viewer_main_signal[1:]
        #     self.viewer_main_signal.extend(temp_viewer_main_signal)
        #     self.viewer_main_signal_time_points_array = np.linspace(0 , (self.viewer_main_signal_time_points_array[-1] * 2)  , self.viewer_main_signal_time_points_length * 2)
        #     self.reconstuction_time_interval = np.linspace(0 , self.reconstuction_time_interval[-1] * 2  , self.viewer_main_signal_time_points_length * 2)
        #     # self.viewer_main_signal_time_points_array = np.arange(0 , (self.viewer_main_signal_time_points_array[-1] * 2)  , (self.viewer_main_signal_time_points_array[1] - self.viewer_main_signal_time_points_array[0]))
        #     # self.reconstuction_time_interval = np.arange(0 , self.reconstuction_time_interval[-1] * 2  , (self.reconstuction_time_interval[1] - self.reconstuction_time_interval[0]))
        #     self.sample_viewer_main_signal()
        # self.viewer_main_signal = np.array(self.viewer_main_signal)
        return sampled_time_values , sampled_signal_values
        # for single_signal_component in self.viewer_main_signal_components:
        #     sampled_signal_values += single_signal_component.amplitude * np.sin(2 * np.pi * sampled_time_values * single_signal_component.frequency)
            
    def calculate_reconstruction_error_without_noise(self):
        self.viewer_main_signal_reconstruction_error = self.viewer_main_signal - self.reconstructed_signal
        return self.viewer_main_signal_reconstruction_error
    
    def calculate_reconstruction_error_with_noise(self , original_signal):
        self.viewer_main_signal_reconstruction_error = original_signal - self.reconstructed_signal
        return self.viewer_main_signal_reconstruction_error
    
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
    
    def apply_fourier_transform_viewer_reconstructed_signal(self):
        main_viewer_signal_fft = np.fft.rfft(self.reconstructed_signal)
        main_viewer_signal_fft_positive_magnitudes = np.abs(main_viewer_signal_fft)
        main_viewer_signal_frequencies = np.fft.rfftfreq(self.viewer_main_signal_time_points_length, self.viewer_main_signal_time_points_array[1] - self.viewer_main_signal_time_points_array[0])
        
        return main_viewer_signal_frequencies , main_viewer_signal_fft_positive_magnitudes
        
    def calcualte_loaded_signal_sample_rate(self):
        csv_signal = pd.read_csv('emg.csv')
        time_diffs_between_two_samples = csv_signal['time'].diff().dropna()
        csv_signal_delta_t = time_diffs_between_two_samples.mean()
        csv_signal_sample_rate = 1 / csv_signal_delta_t
        return csv_signal_sample_rate
