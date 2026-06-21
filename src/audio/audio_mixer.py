import sounddevice as sd
import numpy as np

from src.audio.sound_manager import SoundManager


class AudioMixer:
    def __init__(self, app, sound_manager):
        self.app = app

        self.stream = None
        self.sound_manager = sound_manager

    def find_vbcable(self):

        for index, device in enumerate(sd.query_devices()):
            name = device["name"].lower()
            if "cable input" in name and device["max_output_channels"] > 0:
                #print("--->", index)
                return index

        return None
    
    def start_micro_passthrough(self, input_device, output_device):

        self.stop()

        def callback(indata, outdata, frames, time, status):
            soundboard = self.get_soundboard_buffer(frames)
            #print(np.max(np.abs(soundboard)))
            mic_gain = self.app.parameters["microphone_volume"]
            mixed = indata * mic_gain + soundboard
            mixed = np.clip(mixed,-1.0,1.0)
            outdata[:] = mixed

        self.stream = sd.Stream(
            device = (input_device,output_device),
            channels = (2,2),
            samplerate = 48000,
            callback = callback
        )

        self.stream.start()

    def get_soundboard_buffer(self, frames):
        #print(len(self.sound_manager.active_sounds))
        mixed = np.zeros((frames, 2), dtype=np.float32)

        finished = []

        for sound in self.sound_manager.active_sounds:
            samples = sound["samples"]

            start = sound["position"]
            end = start + frames

            chunk = samples[start:end]

            if len(chunk) < frames:
                padding = np.zeros((frames - len(chunk), 2),dtype=np.float32)
                chunk = np.vstack(
                    [chunk, padding]
                )

                finished.append(sound)

            mixed += chunk * sound["volume"]
            sound["position"] += frames

        for sound in finished:
            self.sound_manager.active_sounds.remove(sound)

        return mixed

    def stop(self):

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None