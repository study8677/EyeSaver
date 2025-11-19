import customtkinter as ctk
from .config_manager import ConfigManager

class SettingsGUI:
    def __init__(self, config_manager: ConfigManager, on_save_callback=None):
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback
        self.window = None

    def show(self):
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.focus()

    def create_window(self):
        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.window = ctk.CTk()
        self.window.title("护眼提醒设置")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        # Title
        title_label = ctk.CTkLabel(self.window, text="设置", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Work Duration
        self.work_var = ctk.StringVar(value=str(self.config_manager.get("work_duration")))
        work_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        work_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(work_frame, text="工作时长 (分钟):").pack(side="left")
        ctk.CTkEntry(work_frame, textvariable=self.work_var, width=100).pack(side="right")

        # Sound Toggle
        self.sound_var = ctk.BooleanVar(value=self.config_manager.get("sound_enabled"))
        sound_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        sound_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(sound_frame, text="声音提醒:").pack(side="left")
        ctk.CTkSwitch(sound_frame, text="", variable=self.sound_var, onvalue=True, offvalue=False).pack(side="right")

        # Save Button
        save_button = ctk.CTkButton(self.window, text="保存", command=self.save_settings)
        save_button.pack(pady=30)

        self.window.mainloop()

    def save_settings(self):
        try:
            work_duration = int(self.work_var.get())
            sound_enabled = self.sound_var.get()
            
            self.config_manager.set("work_duration", work_duration)
            self.config_manager.set("sound_enabled", sound_enabled)
            
            if self.on_save_callback:
                self.on_save_callback()
            
            self.window.destroy()
        except ValueError:
            # Simple error handling (could be improved with a dialog)
            print("Invalid input")

if __name__ == "__main__":
    # Test
    cm = ConfigManager()
    gui = SettingsGUI(cm)
    gui.show()
