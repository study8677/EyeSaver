import customtkinter as ctk
from config_manager import ConfigManager
import threading
import time

class DashboardGUI:
    def __init__(self, config_manager: ConfigManager, app_controller):
        self.config_manager = config_manager
        self.app = app_controller
        self.window = None
        self.update_job = None

    def show(self):
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.focus()
            self.window.lift()

    def create_window(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Eye Saver Dashboard")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Handle close event (minimize to tray)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Main Layout
        self.setup_ui()
        
        # Start update loop
        self.update_ui_loop()
        
        self.window.mainloop()

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title = ctk.CTkLabel(header_frame, text="Eye Saver", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")
        
        # Stats Cards
        stats_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.today_card = self.create_stat_card(stats_frame, "今日休息", "0 次")
        self.today_card.pack(side="left", expand=True, fill="both", padx=5)
        
        self.total_card = self.create_stat_card(stats_frame, "累计休息", "0 次")
        self.total_card.pack(side="right", expand=True, fill="both", padx=5)

        # Progress Section
        progress_frame = ctk.CTkFrame(self.window)
        progress_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.status_label = ctk.CTkLabel(progress_frame, text="工作中...", font=ctk.CTkFont(size=16))
        self.status_label.pack(pady=(20, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=300, height=15)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.time_label = ctk.CTkLabel(progress_frame, text="00:00 / 50:00", font=ctk.CTkFont(size=14, text_color="gray"))
        self.time_label.pack(pady=5)

        # Controls
        controls_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        controls_frame.pack(pady=20, padx=20, fill="x")
        
        self.pause_btn = ctk.CTkButton(controls_frame, text="暂停计时", command=self.toggle_pause, width=120)
        self.pause_btn.pack(side="left", padx=10)
        
        self.settings_btn = ctk.CTkButton(controls_frame, text="设置", command=self.open_settings, width=120, fg_color="gray")
        self.settings_btn.pack(side="right", padx=10)

    def create_stat_card(self, parent, title, value):
        frame = ctk.CTkFrame(parent)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12)).pack(pady=(10, 0))
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=20, weight="bold"))
        value_label.pack(pady=(0, 10))
        # Store reference to update later
        frame.value_label = value_label
        return frame

    def update_ui_loop(self):
        if self.window and self.window.winfo_exists():
            # Update Stats
            stats = self.config_manager.get("stats")
            self.today_card.value_label.configure(text=f"{stats.get('today_rests', 0)} 次")
            self.total_card.value_label.configure(text=f"{stats.get('total_rests', 0)} 次")
            
            # Update Progress
            if self.app:
                elapsed = time.time() - self.app.last_rest_time
                duration_min = self.config_manager.get("work_duration")
                duration_sec = duration_min * 60
                
                progress = min(elapsed / duration_sec, 1.0)
                self.progress_bar.set(progress)
                
                elapsed_min = int(elapsed // 60)
                elapsed_sec = int(elapsed % 60)
                self.time_label.configure(text=f"{elapsed_min:02d}:{elapsed_sec:02d} / {duration_min:02d}:00")
                
                if self.app.paused:
                    self.status_label.configure(text="已暂停", text_color="orange")
                    self.pause_btn.configure(text="继续计时")
                else:
                    self.status_label.configure(text="工作中...", text_color="green") # Default color
                    self.pause_btn.configure(text="暂停计时")

            self.window.after(1000, self.update_ui_loop)

    def toggle_pause(self):
        if self.app:
            self.app.paused = not self.app.paused
            # UI update happens in loop

    def open_settings(self):
        # Simple settings dialog
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("设置")
        dialog.geometry("300x200")
        dialog.grab_set() # Modal
        
        ctk.CTkLabel(dialog, text="工作时长 (分钟):").pack(pady=10)
        entry = ctk.CTkEntry(dialog)
        entry.insert(0, str(self.config_manager.get("work_duration")))
        entry.pack(pady=5)
        
        sound_var = ctk.BooleanVar(value=self.config_manager.get("sound_enabled"))
        ctk.CTkSwitch(dialog, text="声音提醒", variable=sound_var).pack(pady=10)
        
        def save():
            try:
                val = int(entry.get())
                self.config_manager.set("work_duration", val)
                self.config_manager.set("sound_enabled", sound_var.get())
                dialog.destroy()
            except ValueError:
                pass
        
        ctk.CTkButton(dialog, text="保存", command=save).pack(pady=20)

    def on_close(self):
        self.window.withdraw() # Hide window
