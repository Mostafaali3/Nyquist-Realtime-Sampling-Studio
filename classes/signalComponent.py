import numpy as np
class SignalComponent():
    def __init__(self, amplitude, frequency, shift):
        self.__amplitude = amplitude
        self.__frequency = frequency
        self.__shift = shift
        self.__id = np.random.randint(100000, size=1)[0]
        