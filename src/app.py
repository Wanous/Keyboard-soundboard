import customtkinter as ctk
import keyboard
import mouse
import platform

from src.audio.sound_manager import SoundManager
from src.audio.microphone_manager import MicrophoneManager
from src.audio.audio_mixer import AudioMixer

from src.ui.microphone_frame import MicrophoneFrame
from src.ui.sound_list_frame import SoundListFrame

from src.utils.config import ConfigManager
from src.utils.resource_path import resource_path



class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Soundboard")
        self.iconbitmap(str(resource_path("assets/icon/icon.ico")))
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW",self.on_close)

        # Managers
        self.microphone_manager = MicrophoneManager()
        self.config_manager = ConfigManager()
        self.sound_manager = SoundManager(self, self.config_manager.SOUNDS_DIR)
        self.audio_mixer = AudioMixer(self, self.sound_manager)

        # Datas
        self.config = self.config_manager.load_config()
        self.shortcuts = self.config["sound_datas"]
        self.parameters = self.config["parameters"]

        self.selected_microphone = None

        self.hotkeys = []
        self.register_shortcuts()

        # VB Cable
        vb = self.audio_mixer.find_vbcable()

        self.vb_device = (
        self.audio_mixer.find_vbcable()
        )

        self.audio_mixer.start_micro_passthrough(
                    input_device=self.selected_microphone,
                    output_device=self.vb_device
        )

        # Parameters
        self.local_playback_enabled = ctk.BooleanVar(value = self.parameters["local_playback_enabled"])
        mouse.on_middle_click(self.sound_manager.stop_all)
        self.microphone_volume = ctk.DoubleVar(value = self.parameters["microphone_volume"])
        self.default_microphone = ctk.StringVar(value = self.parameters["default_microphone"])

        self.create_widgets()

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.grid_rowconfigure(0, weight=1)

        self.microphone_frame = MicrophoneFrame(self)
        self.microphone_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.sound_frame = SoundListFrame(self)
        self.sound_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

    def register_shortcuts(self):

        for hotkey in self.hotkeys:
            keyboard.remove_hotkey(hotkey)

        self.hotkeys.clear()

        # Sounds shortcut

        for filename, data in self.shortcuts.items():

            shortcut = data.get("shortcut")

            if not shortcut:
                continue

            hotkey = keyboard.add_hotkey(
                shortcut,
                lambda f=filename:
                    self.sound_manager.play(f)
            )

            self.hotkeys.append(hotkey)

        # Stop All shortcut

        panic_shortcut = self.parameters.get("panic_shortcut","ctrl")
        panic_hotkey = keyboard.add_hotkey(panic_shortcut,self.sound_manager.stop_all)

        self.hotkeys.append(panic_hotkey)
        
    def save_config(self):
        self.config_manager.save_config(self.config)
        self.register_shortcuts() # Refresh shortcut search
    
    def on_close(self):
        keyboard.unhook_all()
        self.sound_manager.teardown()
        self.destroy()

 