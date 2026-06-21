import customtkinter as ctk

class ShortcutDialog(ctk.CTkToplevel):

    def __init__(self, app, filename, item_widget, sender = "sound_shortcut"):

        super().__init__()

        self.transient(app)
        self.grab_set()
        self.focus_force()

        self.app = app
        self.filename = filename
        self.item_widget = item_widget
        self.sender = sender # To know if send for a sound shortcut or a another shortcut

        self.current_keys = set()

        self.label = ctk.CTkLabel(
            self,
            text="Appuyez sur la combinaison"
        )

        self.label.pack(
            padx=20,
            pady=10
        )

        self.display = ctk.CTkLabel(
            self,
            text=""
        )

        self.display.pack(
            padx=20,
            pady=10
        )

        self.ok_button = ctk.CTkButton(
            self,
            text="OK",
            command=self.validate
        )

        self.ok_button.pack(
            pady=10
        )

        self.bind("<KeyPress>", self.on_press)

    def on_press(self, event):

        key = event.keysym.lower()

        if key not in self.current_keys:
            self.current_keys.add(key)

        self.display.configure(text="+".join(sorted(self.current_keys)))

    def validate(self):

        shortcut = "+".join(sorted(self.current_keys))

        if self.sender != "sound_shortcut":
            self.app.parameters[self.sender] = shortcut
            self.app.save_config()
            self.item_widget.configure(text=shortcut)
            self.close()
        else:
            self.app.shortcuts[self.filename] = {"shortcut": shortcut}

        self.app.save_config()

        self.item_widget.refresh_shortcut_text()

        self.close()

    def close(self):

        self.grab_release()
        self.destroy()