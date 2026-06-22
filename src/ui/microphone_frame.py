import customtkinter as ctk
import sounddevice as sd


class MicrophoneFrame(ctk.CTkFrame):

    def __init__(self, app):

        super().__init__(app)

        self.app = app

        microphones = self.app.microphone_manager.get_microphones()
        saved_index = self.app.parameters.get("default_microphone")

        values = [mic["name"] for mic in microphones]

        self.label = ctk.CTkLabel(self,text="Microphone")

        self.label.pack(
            padx=10,
            pady=(10, 5)
        )

        self.combo = ctk.CTkComboBox(
            self,
            values=values,
            command=self.on_microphone_selected
        )

        for mic in microphones:
            if mic["index"] == saved_index:
                self.combo.set(mic["name"])
                self.on_microphone_selected(mic["name"])
                break

        self.combo.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        self.level_bar = ctk.CTkProgressBar(
            self
        )

        self.level_bar.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.level_bar.set(0)

        self.volume_label = ctk.CTkLabel(
            self,
            text="Microphone volume"
        )

        self.volume_label.pack(
            padx=10,
            pady=(10, 0)
        )
        
        self.volume_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=2,
            variable = self.app.microphone_volume,
            command = self.on_micro_volume_changed
        )

        self.volume_slider.pack(
            fill="x",
            padx=10,
            pady=10
        )
        self.update_level_meter()

    def on_microphone_selected(self, selected_name):

        microphones = self.app.microphone_manager.get_microphones()

        for mic in microphones:
            if mic["name"] == selected_name:
                self.app.selected_microphone = mic
                self.app.microphone_manager.start_monitoring(mic["index"])
                self.app.parameters["default_microphone"] = mic["index"]
                self.app.save_config()
                break
            
    def on_micro_volume_changed(self, value):
        self.app.parameters["microphone_volume"] = value
        self.app.save_config()

    def update_level_meter(self):

        level = self.app.microphone_manager.get_level()
        level = min(level * 10, 1.0)

        self.level_bar.set(level)

        self.after(30,self.update_level_meter)
