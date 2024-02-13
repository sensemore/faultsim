import numpy as np
from equipment import Equipment

class Coupling(Equipment):
    def __init__(self, properties):
        super().__init__('coupling', properties)

    def generate_vibration_signal(self, rpm,duration, sampling_rate):
        t, signal = super().generate_vibration_signal(rpm,duration, sampling_rate)
        # Coupling-specific vibration simulation
        misalignment = self.properties.get('misalignment', 0.1)
        wear = self.properties.get('wear', 0.05)
        signal += misalignment * np.cos(2 * np.pi * 10 * t) + wear * np.sin(2 * np.pi * 5 * t)
        return t, signal
