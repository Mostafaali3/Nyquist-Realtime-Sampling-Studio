from signalComponent import SignalComponent
import numpy as np
import matplotlib.pyplot as plt
class Mixer():
    def __init__(self):
        pass
    
    
    def make_signal(self, signal_components):
        final_signal = np.zeros(1000)
        print(len(final_signal))
        for component in signal_components:
            line = np.linspace(0,20, 1000)
            wave = component.amplitude * np.sin(np.dot(2*np.pi*component.frequency, line) + component.shift)
            final_signal = final_signal + wave
        return final_signal
    
    
mix = Mixer()
comp1 = SignalComponent(amplitude=0.6, frequency=0.5, shift=0, id=1)
comp2 = SignalComponent(amplitude=0.4, frequency=0.7, shift=0, id=1)
components = [comp1, comp2]
signal = mix.make_signal(components)
print(signal)

plt.plot(np.linspace(0, 20, 1000), signal)
plt.show()