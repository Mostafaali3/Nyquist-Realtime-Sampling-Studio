import numpy as np

class Noiser:
    def __init__(self):
        pass
        
    def generate_noise(self , signal: np.ndarray, snr: float) -> np.ndarray:
        self.signal = signal.signal[1]
        self.signal = np.array(self.signal)
        self.snr = snr
        signal_power = np.mean(self.signal ** 2)
        snr_linear = 10 ** (self.snr / 10)
        noise_power = signal_power / snr_linear
        noise = np.random.normal(0, np.sqrt(noise_power), self.signal.shape)
        return noise