import time
import threading
import os
import sys
import winsound
from PIL import Image, ImageDraw
from pystray import Icon, MenuItem, Menu
from plyer import notification

from src.config_manager import ConfigManager
from src.settings_gui import SettingsGUI

class EyeSaverApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.settings_gui = SettingsGUI(self.config_manager, self.on_settings_saved)
        
        self.running = True
        self.paused = False
        self.icon = None
        self.timer_thread = None
        self.last_rest_time = time.time()

    def create_image(self):
        # Create a simple icon image
        width = 64
        height = 64
        color1 = "blue"
        color2 = "white"
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=color2)
        dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=color2)
        return image

    def play_sound(self):
        if self.config_manager.get("sound_enabled"):
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                pass

    def notify_rest(self):
        self.play_sound()
        notification.notify(
            title='护眼提醒',
            message=f'已经工作 {self.config_manager.get("work_duration")} 分钟了，请休息一下眼睛！',
            app_name='Eye Saver',
            timeout=10
        )

    def timer_loop(self):
        while self.running:
            if self.paused:
                time.sleep(1)
                continue

            work_duration_minutes = self.config_manager.get("work_duration")
            # Check every second
            if time.time() - self.last_rest_time >= work_duration_minutes * 60:
                if self.running and not self.paused:
                    self.notify_rest()
                    self.last_rest_time = time.time()
            
            time.sleep(1)

    def on_quit(self, icon, item):
        self.running = False
        icon.stop()
        sys.exit(0)

    def on_settings(self, icon, item):
        # Launch GUI in the main thread (or separate process if needed, but here we just invoke it)
        # Note: pystray runs in its own thread usually. 
        # Tkinter needs to run in the main thread. 
        # Since we started pystray in the main thread (app.run -> icon.run), 
        # we can't easily run tkinter alongside it in the SAME thread without conflict.
        # A common workaround is to run tkinter in a separate process or thread, 
        # but tkinter MUST be in the main thread usually.
        # 
        # Correction: pystray `icon.run()` blocks. 
        # So we need to run the timer in a thread (done).
        # And we need to run the GUI. 
        # Since `icon.run()` is blocking the main thread, we have a problem launching tkinter.
        # 
        # Solution: We will run the GUI in a separate process using multiprocessing 
        # OR we can try to run it in a thread (might be unstable).
        # 
        # BETTER SOLUTION for simple app: 
        # Run the Settings GUI in a separate thread? No, tkinter hates that.
        # 
        # Let's try running the GUI in a separate PROCESS.
        # This avoids GIL and threading issues with GUI frameworks.
        import multiprocessing
        p = multiprocessing.Process(target=self.open_settings_process)
        p.start()

    def open_settings_process(self):
        # Re-instantiate config manager in new process
        cm = ConfigManager()
        gui = SettingsGUI(cm)
        gui.show()

    def on_settings_saved(self):
        # Reload config
        self.config_manager = ConfigManager() # Reload from file
        print("Settings updated")

    def on_toggle_pause(self, icon, item):
        self.paused = not self.paused
        # Update menu text (requires pystray update mechanism, which is tricky with simple menu)
        # For now, just toggle. Ideally we update the icon or tooltip.
        state = "暂停" if self.paused else "运行"
        self.icon.notify(f"计时器已{state}")

    def run(self):
        # Start timer in a separate thread
        self.timer_thread = threading.Thread(target=self.timer_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()

        # Setup system tray icon
        image = self.create_image()
        menu = Menu(
            MenuItem('设置', self.on_settings),
            MenuItem('暂停/继续', self.on_toggle_pause),
            MenuItem('退出', self.on_quit)
        )
        self.icon = Icon("Eye Saver", image, "护眼提醒", menu)
        
        # self.notify_rest() # Optional start notification
        
        self.icon.run()

if __name__ == "__main__":
    # Multiprocessing support for Windows
    import multiprocessing
    multiprocessing.freeze_support()
    
    app = EyeSaverApp()
    app.run()
