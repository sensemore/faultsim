import numpy as np
from equipment import Equipment

class Bearing(Equipment):
    def __init__(self, properties):
        super().__init__('bearing', properties)

    def apply_transfer_function(self, input_signal, t):
        # Add defect signals based on the defect type
        defect_type = self.properties.get('defect_type', 'inner_race')

        if defect_type == 'inner_race':
            input_signal += self.inner_race_defect_signal(t)
        elif defect_type == 'outer_race':
            input_signal += self.outer_race_defect_signal(t)
        elif defect_type == 'ball':
            input_signal += self.ball_defect_signal(t)
        elif defect_type == 'cage':
            input_signal += self.cage_defect_signal(t)
        
        return input_signal

    def inner_race_defect_signal(self, t):
        signal = 0.1 * np.sin(2 * np.pi * self.properties.get('BPFI', 100) * t)
        return signal

    def outer_race_defect_signal(self, t):
        signal = 0.1 * np.sin(2 * np.pi * self.properties.get('BPFO', 90) * t)
        return signal

    def ball_defect_signal(self, t):
        signal = 0.1 * np.sin(2 * np.pi * self.properties.get('BSF', 50) * t)
        return signal

    def cage_defect_signal(self, t):
        signal = 0.1 * np.sin(2 * np.pi * self.properties.get('FTF', 10) * t)
        return signal

    def generate_vibration_signal(self,rpm, duration, sampling_rate):
        t, signal = super().generate_vibration_signal(rpm,duration, sampling_rate)
        # Override with bearing-specific simulation using defect frequencies
        bpfi = self.properties.get('BPFI', 100)*rpm
        bpfo = self.properties.get('BPFO', 90)*rpm
        bsf = self.properties.get('BSF', 50)*rpm
        ftf = self.properties.get('FTF', 10)*rpm
        
        signal += np.sin(2 * np.pi * bpfi * t) + np.sin(2 * np.pi * bpfo * t)
        signal += np.sin(2 * np.pi * bsf * t) + np.sin(2 * np.pi * ftf * t)

        return t, signal
