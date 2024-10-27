import numpy as np

class Noiser:
    def __init__(self, signal: np.ndarray, snr: float):
        self.signal = signal
        self.snr = snr
        
    def generate_noise(self) -> np.ndarray:
        signal_power = np.mean(self.signal ** 2)
        snr_linear = 10 ** (self.snr / 10)
        noise_power = signal_power / snr_linear
        noise = np.random.normal(0, np.sqrt(noise_power), self.signal.shape)
        return noise