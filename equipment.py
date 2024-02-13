import numpy as np
import random
import string
class Equipment:
    def __init__(self, type,properties):
        self.name = "".join([random.choice(string.ascii_uppercase) for i in range(5)])
        self.type = type
        self.properties = properties
        self.next_equipment = None  # To hold the next equipment in the chain

    def connect(self, equipment):
        self.next_equipment = equipment
        return equipment  # Return the next equipment for chaining
    def apply_transfer_function(self, input_signal, t):
        return input_signal
    def generate_vibration_signal(self,rpm, duration, sampling_rate):
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        signal = np.sin(2 * np.pi * rpm * t)
        return t, signal
    
    def update_properties(self, new_properties):
        self.properties.update(new_properties)
        return

    def drive(self, rpm, duration):
        # Convert rpm and duration to appropriate units if necessary
        duration_sec = float(duration)
        sampling_rate = 1000  # Example sampling rate

        # Generate vibration signal for the current equipment
        t, signal = self.generate_vibration_signal(rpm,duration_sec, sampling_rate)

        # Apply transfer function to the signal
        signal = self.apply_transfer_function(signal, t)

        # If there's next equipment, call its drive method and accumulate the signal
        if self.next_equipment is not None:
            _, next_signal = self.next_equipment.drive(rpm, duration)
            signal += next_signal  # Example way to combine signals

        return t, signal
