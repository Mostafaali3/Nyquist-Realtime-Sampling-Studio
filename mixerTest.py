import numpy as np
import pandas as pd

# Parameters
num_points = 1000
x_max = 20
amplitude = 1  # Set the amplitude of the rectangular signal
frequency = 1  # Set the frequency of the rectangular signal

# Generate x values
x_values = np.linspace(0, x_max, num_points)

# Generate rectangular wave (square wave) with given frequency
signal_values = amplitude * np.sign(np.sin(2 * np.pi * frequency * x_values / x_max))

# Create a DataFrame and save to CSV
df = pd.DataFrame({'Time [s]': x_values, ' II': signal_values})
df.to_csv('rectangular_signal.csv', index=False)
