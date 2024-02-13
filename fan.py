import numpy as np
from equipment import Equipment

class Fan(Equipment):
    def __init__(self, properties):
        super().__init__('fan', properties)

    def generate_vibration_signal(self,rpm, duration, sampling_rate):
        t, signal = super().generate_vibration_signal(rpm,duration, sampling_rate)
        # Fan-specific vibration simulation
        blade_pass_freq = self.properties.get('Blade Pass Frequency', 120)
        imbalance = self.properties.get('Imbalance', 0.2)
        signal += imbalance * np.sin(2 * np.pi * blade_pass_freq * t)
        return t, signal