import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


def generate_noise(signal: np.ndarray, snr: float) -> np.ndarray:
    signal_power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr / 10)
    noise_power = signal_power / snr_linear
    noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
    return noise

# Main PyQt Application
class SignalApp(QMainWindow):
    def __init__(self, signal, snr):
        super().__init__()
        
        noise = generate_noise(signal, snr)
        noisy_signal = signal + noise
        
        self.setWindowTitle("Signal and Noisy Signal")
        self.setGeometry(100, 100, 800, 400)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.original_plot = pg.PlotWidget(title="Original Signal")
        self.original_plot.plot(signal, pen=pg.mkPen(color='b', width=2), name="Original Signal")
        layout.addWidget(self.original_plot)
        
        self.noisy_plot = pg.PlotWidget(title="Noisy Signal (SNR = {} dB)".format(snr))
        self.noisy_plot.plot(noisy_signal, pen=pg.mkPen(color='r', width=2), name="Noisy Signal")
        layout.addWidget(self.noisy_plot)

if __name__ == "__main__":
    x = np.linspace(0, 2 * np.pi, 500)
    signal = np.sin(5 * x)  
    snr = 10  
    
    app = QApplication(sys.argv)
    window = SignalApp(signal, snr)
    window.show()
    sys.exit(app.exec_())
