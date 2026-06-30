from tkinter import messagebox
import customtkinter as ctk

from src.ui.shortcut_dialog import ShortcutDialog

class SoundItemWidget(ctk.CTkFrame):

    def __init__(self, parent, app, filename):

        super().__init__(parent)

        self.app = app
        self.filename = filename

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(
            self,
            text=self.filename
        )

        self.name_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(5, 0)
        )

        self.play_button = ctk.CTkButton(
            self,
            text="▶",
            width=40,
            command=self.play
        )

        self.play_button.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(10, 0),
            pady=5
        )

        self.stop_button = ctk.CTkButton(
            self,
            text="■",
            width=40,
            command=self.stop
        )

        self.stop_button.grid(
            row=1,
            column=0,
            sticky="w",
            padx=60
        )

        self.volume_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=0.5,
            command=self.on_volume_change
        )

        self.volume_slider.grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        volume = self.app.shortcuts.get(self.filename, {}).get("volume", 0.25)
        self.volume_slider.set(volume)

        self.shortcut_button = ctk.CTkButton(
            self,
            text=self.get_shortcut_text(),
            command=self.open_shortcut_dialog
        )

        self.shortcut_button.grid(
            row=1,
            column=2,
            padx=5
        )

        self.delete_button = ctk.CTkButton(
            self,
            text="✕",
            width=40,
            command=self.delete
        )

        self.delete_button.grid(
            row=1,
            column=3,
            padx=(5, 10)
        )

    def play(self):
        self.app.sound_manager.play(self.filename)

    def stop(self):
        self.app.sound_manager.stop(self.filename)

    def delete(self):

        answer = messagebox.askyesno(
            "Suppression",
            f"Supprimer '{self.filename}' ?"
        )

        if not answer:
            return

        self.app.sound_manager.delete_sound(self.filename)
        self.app.shortcuts.pop(self.filename,None)
        self.app.register_shortcuts()
        self.app.sound_frame.refresh()

    def open_shortcut_dialog(self):

        ShortcutDialog(
            app=self.app,
            filename=self.filename,
            item_widget=self
        )

    def refresh_shortcut_text(self):

        shortcut = self.app.shortcuts.get(self.filename, {}).get("shortcut", "Raccourci")
        self.shortcut_button.configure(text=shortcut)
        
    def get_shortcut_text(self):
        try:
            shortcut = self.app.shortcuts[self.filename]['shortcut']
        except Exception:
            shortcut = "Raccourci"

        return shortcut

    def on_volume_change(self, value):

        if self.filename not in self.app.shortcuts:
            self.app.shortcuts[self.filename] = {}

        self.app.shortcuts[self.filename]["volume"] = round(value, 2)
        self.app.save_config()

