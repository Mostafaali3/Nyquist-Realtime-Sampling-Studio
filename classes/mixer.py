from classes.signalComponent import SignalComponent
import numpy as np
import matplotlib.pyplot as plt
from classes.channel import Channel

class Mixer():
    def __init__(self):
        pass
    
    
    def mix_signal(self, signal_components):
        '''
        make sure that the input is dict not list 
        '''
        final_signal = np.zeros(1000)
        print(len(final_signal))
        for key, component in signal_components.items():
            line = np.linspace(0,20, 1000)
            wave = component.amplitude * np.sin(np.dot(2*np.pi*component.frequency, line) + component.shift)
            final_signal = final_signal + wave
            
        composed_signal = Channel(line, final_signal, signal_components)
        return composed_signal
    
    
# mix = Mixer()
# comp1 = SignalComponent(amplitude=0.6, frequency=0.5, shift=0, id=1)
# comp2 = SignalComponent(amplitude=0.4, frequency=0.7, shift=0, id=1)
# components = [comp1, comp2]
# signal = mix.make_signal(components)
# print(signal)

# plt.plot(np.linspace(0, 20, 1000), signal)
# plt.show()