from src.app import App
import customtkinter as ctk
from src.utils.resource_path import resource_path


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme(str(resource_path("assets/themes/lavender.json")))

    app = App()
    app.mainloop()
