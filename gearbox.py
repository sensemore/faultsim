import numpy as np
from equipment import Equipment

class Gearbox(Equipment):
    def __init__(self, properties):
        super().__init__('gearbox', properties)
    def generate_vibration_signal(self, rpm,duration, sampling_rate):
        t, signal = super().generate_vibration_signal(rpm,duration, sampling_rate)
        # Gearbox-specific vibration simulation
        gear_mesh_freq = self.properties.get('Gear Mesh Frequency', 200)
        misalignment = self.properties.get('Misalignment', 0.2)
        wear = self.properties.get('Wear', 0.1)

        signal += np.sin(2 * np.pi * gear_mesh_freq * t) + misalignment * np.sin(2 * np.pi * 3 * t) + wear * np.sin(2 * np.pi * 1.5 * t)
        return t, signal