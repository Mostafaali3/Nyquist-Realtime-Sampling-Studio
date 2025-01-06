# Sampling-Theory Studio
![Application Overview](icons_setup/icons/task_2_image.png "Overview of Sampling Studio")
## Overview
This project is a desktop application developed to demonstrate the principles of signal sampling and recovery based on the Nyquist–Shannon sampling theorem. It helps users visualize, sample, and reconstruct signals using various methods, showcasing the impact of sampling frequency and noise on signal recovery.

---

## Features
1. **Signal Sampling and Recovery**:
   - Load a signal (from a file or generated in-app) and visualize it.
   - Sample the signal at different frequencies (normalized or actual).
   - Recover the original signal using various reconstruction methods like Whittaker–Shannon interpolation.

2. **Signal Mixer/Composer**:
   - Combine sinusoidal signals of different frequencies and amplitudes.
   - Add or remove components dynamically.
![Video Demo](assets/mixing%20(1).gif)
[Watch the video](assets/mixing.mp4)
3. **Noise Addition**:
   - Add controllable noise to the signal with a customizable SNR.
   - Visualize the effect of noise on signal frequency.
![Video Demo](assets/Noise_add.gif)
[Watch the video](assets/Noise_add.mp4)
4. **Real-Time Interaction**:
   - Changes in sampling frequency and reconstruction methods update the visualization in real time.

5. **Reconstruction Methods**:
   - Explore multiple reconstruction techniques, including Whittaker–Shannon and alternatives, via a dropdown menu.
![Video Demo](assets/sampling_mehods.gif)
[Watch the video](assets/sampling_mehods.mp4)
6. **Multiple Graphs**:
   - View the original signal, reconstructed signal, error (difference), and frequency domain in a convenient layout.

7. **Responsive UI**:
   - The application adjusts dynamically to resizing without disrupting the interface.

8. **Testing Scenarios**:
   - Includes test cases demonstrating scenarios like aliasing and signal reconstruction challenges.


---

## Dependencies

The Multi-Signal Viewer relies on the following technologies and libraries to deliver its robust functionality:

| **Dependency**       | **Description**                                       |
|-----------------------|-------------------------------------------------------|
| Python 3.x           | Core programming language.                            |
| NumPy                | Numerical computations for signal processing.         |
| Pandas               | Data manipulation and analysis.                       |
| SciPy                | Advanced scientific computing and interpolation.      |
| PyQt5                | GUI framework for building desktop applications.      |
| PyQtGraph            | Fast plotting and 2D/3D visualization in PyQt.        |

---

## Setup Instructions
#### Clone the repository
```bash
git clone https://github.com/Mostafaali3/Nyquist-Realtime-Sampling-Studio.git
```
#### Navigate to project directory
```bash
cd Nyquist-Realtime-Sampling-Studio
```

#### Install required packages
```bash
pip install -r requirements.txt
```

#### Run the application
```bash
python main.py
```

---

## Contributors <a name="Contributors"></a>
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Mostafaali3" target="_blank">
        <img src="https://github.com/Mostafaali3.png" width="150px;" alt="Mostafa Ali"/>
        <br />
        <sub><b>Mostafa Ali</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Youssef-Abo-El-Ela" target="_blank">
        <img src="https://github.com/Youssef-Abo-El-Ela.png" width="150px;" alt="Youssef Abo El Ela"/>
        <br />
        <sub><b>Youssef Abo El-Ela</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/karreemm" target="_blank">
        <img src="https://github.com/karreemm.png" width="150px;" alt="Kareem Abdel Nabi"/>
        <br />
        <sub><b>Kareem Abdel Nabi</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/AhmedXAlDeeb" target="_blank">
        <img src="https://github.com/AhmedXAlDeeb.png" width="150px;" alt="Ahmed X AlDeeb"/>
        <br />
        <sub><b>Ahmed AlDeeb</b></sub>
      </a>
    </td>
  </tr>
</table>
