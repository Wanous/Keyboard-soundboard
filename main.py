from src.app import App
import customtkinter as ctk
import sys
from pathlib import Path


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("src\\assets\\themes\\lavender.json")

    app = App()
    app.mainloop()
