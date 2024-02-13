import numpy as np

def add_random_noise(signal, noise_level=0.1):
    """
    Adds random Gaussian noise to a signal.
    
    Parameters:
    - signal: The original signal.
    - noise_level: Standard deviation of the noise.
    
    Returns:
    - The signal with added noise.
    """
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise
def add_harmonic_interference(signal, t, interference_freqs=[50, 150], amplitudes=[0.05, 0.02], phases=[0, np.pi/4]):
    """
    Adds harmonic interference to a signal.
    
    Parameters:
    - signal: The original signal.
    - t: Time vector corresponding to the signal.
    - interference_freqs: Frequencies of the harmonic interferences.
    - amplitudes: Amplitudes of the harmonic interferences.
    - phases: Phases of the harmonic interferences.
    
    Returns:
    - The signal with added harmonic interference.
    """
    for freq, amp, phase in zip(interference_freqs, amplitudes, phases):
        signal += amp * np.sin(2 * np.pi * freq * t + phase)
    return signal

def add_transient_spikes(signal, t, spike_times=[1.0, 2.5], spike_amplitude=0.5, spike_duration=0.01):
    """
    Adds transient spikes to a signal.
    
    Parameters:
    - signal: The original signal.
    - t: Time vector corresponding to the signal.
    - spike_times: Times at which spikes occur.
    - spike_amplitude: Amplitude of the spikes.
    - spike_duration: Duration of each spike.
    
    Returns:
    - The signal with added transient spikes.
    """
    sampling_rate = len(t) / (t[-1] - t[0])
    for spike_time in spike_times:
        spike_start = int((spike_time - spike_duration / 2) * sampling_rate)
        spike_end = int((spike_time + spike_duration / 2) * sampling_rate)
        signal[spike_start:spike_end] += spike_amplitude
    return signal