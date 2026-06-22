from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk

from src.ui.sound_item_widget import SoundItemWidget
from src.ui.shortcut_dialog import ShortcutDialog



class SoundListFrame(ctk.CTkFrame):

    def __init__(self, app):

        super().__init__(app)

        self.app = app

        self.listbox = ctk.CTkScrollableFrame(self)

        self.listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.add_button = ctk.CTkButton(
            self,
            text="Add sound",
            command=self.add_sound
        )

        self.add_button.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.buttons_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.stop_all_button = ctk.CTkButton(
            self.buttons_frame ,
            text="⏹ Stop All",
            command=self.app.sound_manager.stop_all
        )

        self.panic_shortcut_button = ctk.CTkButton(
            self.buttons_frame ,
            text=self.app.parameters.get("panic_shortcut", "middle mouse"),
            command=self.open_panic_shortcut_dialog
        )

        self.stop_all_button.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.panic_shortcut_button.pack(
            side="left",
            padx=(5, 0)
        )

        self.monitor_checkbox = ctk.CTkCheckBox(
            self,
            text="Enable local playback",
            variable=self.app.local_playback_enabled,
            command=self.on_local_playback_changed
        )

        self.monitor_checkbox.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.refresh()

    def on_local_playback_changed(self):

        self.app.parameters["local_playback_enabled"] = bool(self.monitor_checkbox.get())
        self.app.save_config()

    def open_panic_shortcut_dialog(self):

        ShortcutDialog(
            self.app,
            "",
            self.panic_shortcut_button,
            "panic_shortcut"
        )

    def refresh(self):

        for widget in self.listbox.winfo_children():
            widget.destroy()

        for sound in self.app.sound_manager.list_sounds():

            label = SoundItemWidget(self.listbox, self.app, sound.name)

            label.pack(
                fill="x",
                padx=5,
                pady=5
            )

    def add_sound(self):

        filename = filedialog.askopenfilename()

        if not filename:
            return

        self.app.sound_manager.add_sound(Path(filename))

        self.refresh()