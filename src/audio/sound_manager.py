from pathlib import Path
import shutil
import pygame
import soundfile as sf
import numpy as np
from scipy.signal import resample


class SoundManager:

    def __init__(self, app, SOUNDS_DIR):
        self.app = app

        self.SOUNDS_DIR = SOUNDS_DIR

        self.active_sounds = [] # List of active sounds
        self.sound_cache = {}   # Store modified/used sound in order to not reload them

        pygame.mixer.init()     # To make make the user heard the sound    

        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._channels: dict[str, pygame.mixer.Channel] = {}

    def load_sound(self, filename):

        if filename in self.sound_cache:
            return self.sound_cache[filename]

        path = self.SOUNDS_DIR / filename
        data, sr = sf.read(str(path),dtype="float32")

        if data.ndim == 1:
            data = np.column_stack([data, data])

        TARGET_SR = 48000

        if sr != TARGET_SR:
            new_length = int(len(data) * TARGET_SR / sr)
            data = resample(data, new_length, axis=0)

        self.sound_cache[filename] = data # Store modified/used sound 

        return data

    def list_sounds(self):
        return sorted(self.SOUNDS_DIR.iterdir())

    def add_sound(self, source):

        destination = self.SOUNDS_DIR / source.name

        shutil.copy2(
            source,
            destination
        )

    def delete_sound(self, filename):

        path = self.SOUNDS_DIR / filename

        if path.exists():
            path.unlink()    
    
    def get_sound(self, filename: str):

        if filename not in self._sounds:
            path = self.SOUNDS_DIR / filename
            self._sounds[filename] = pygame.mixer.Sound(str(path))

        return self._sounds[filename]

    def play(self, filename: str):
        #_______ Local playback part ___________
        volume = self.app.shortcuts.get(filename, {}).get("volume", 1.0)

        if self.app.local_playback_enabled.get():
            sound = self.get_sound(filename)
            sound.set_volume(volume)
            channel = sound.play()

            if channel:
                self._channels[filename] = channel
                samples = self.load_sound(filename)
        
        #_______ VB part ___________
        #print("PLAY:", filename)
        samples = self.load_sound(filename)

        self.active_sounds.append({
            "name": filename,
            "samples": samples,
            "position": 0,
            "volume": volume
        })

    def stop(self, filename: str):

        channel = self._channels.get(filename)

        if channel and channel.get_busy():
            channel.stop()

    def stop_all(self):

        pygame.mixer.stop()
        self._channels.clear()
        self.active_sounds.clear()
        
    def is_playing(self, filename: str):

        channel = self._channels.get(filename)

        return channel is not None and channel.get_busy()

    def teardown(self):
        self.stop_all()
        pygame.mixer.quit()