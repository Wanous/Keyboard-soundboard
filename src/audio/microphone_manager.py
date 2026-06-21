import numpy as np
import sounddevice as sd


class MicrophoneManager:

    def __init__(self):

        self.stream = None
        self.level = 0.0

    def get_microphones(self):

        microphones = []

        for index, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                microphones.append({
                    "index": index,
                    "name": device["name"]
                })

        return microphones

    def start_monitoring(self, device_index):

        self.stop_monitoring()

        def callback(indata, frames, time, status):

            volume = np.sqrt(
                np.mean(indata**2)
            )

            self.level = float(volume)

        self.stream = sd.InputStream(
            device=device_index,
            channels=1,
            callback=callback
        )

        self.stream.start()

    def stop_monitoring(self):

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def get_level(self):

        return self.level