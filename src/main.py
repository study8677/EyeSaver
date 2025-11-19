import time
import threading
import os
import sys
import winsound
from PIL import Image, ImageDraw
from pystray import Icon, MenuItem, Menu
from plyer import notification
import multiprocessing
from multiprocessing import Value

from config_manager import ConfigManager
from dashboard_gui import DashboardGUI

# Standalone function for the dashboard process
def run_dashboard_process(shared_last_rest_time, shared_paused):
    # Re-instantiate config manager in new process
    cm = ConfigManager()
    
    # Create a proxy object to mimic the app controller interface expected by DashboardGUI
    class StateProxy:
        def __init__(self, last_rest_time_val, paused_val):
            self._last_rest_time = last_rest_time_val
            self._paused = paused_val
            
        @property
        def last_rest_time(self):
            return self._last_rest_time.value
            
        @property
        def paused(self):
            return bool(self._paused.value)
            
        @paused.setter
        def paused(self, value):
            self._paused.value = 1 if value else 0

    app_proxy = StateProxy(shared_last_rest_time, shared_paused)
    gui = DashboardGUI(cm, app_proxy) 
    gui.show()

class EyeSaverApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.dashboard_process = None
        
        self.running = True
        # Use shared memory for state that needs to be accessed by the dashboard
        self.shared_paused = Value('i', 0) # 0 for False, 1 for True
        self.shared_last_rest_time = Value('d', time.time())
        
        self.icon = None
        self.timer_thread = None

    @property
    def paused(self):
        return bool(self.shared_paused.value)

    @paused.setter
    def paused(self, value):
        self.shared_paused.value = 1 if value else 0

    @property
    def last_rest_time(self):
        return self.shared_last_rest_time.value

    @last_rest_time.setter
    def last_rest_time(self, value):
        self.shared_last_rest_time.value = value

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
        self.config_manager.increment_rest_count()
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
        if self.dashboard_process and self.dashboard_process.is_alive():
            self.dashboard_process.terminate()
        sys.exit(0)

    def on_open_dashboard(self, icon, item):
        if self.dashboard_process is None or not self.dashboard_process.is_alive():
            # Pass shared values to the new process
            self.dashboard_process = multiprocessing.Process(
                target=run_dashboard_process,
                args=(self.shared_last_rest_time, self.shared_paused)
            )
            self.dashboard_process.start()
        else:
            pass

    def on_toggle_pause(self, icon, item):
        self.paused = not self.paused
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
            MenuItem('打开主面板', self.on_open_dashboard),
            MenuItem('暂停/继续', self.on_toggle_pause),
            MenuItem('退出', self.on_quit)
        )
        self.icon = Icon("Eye Saver", image, "护眼提醒", menu)
        
        # Auto open dashboard on start
        self.on_open_dashboard(None, None)
        
        self.icon.run()

if __name__ == "__main__":
    # Multiprocessing support for Windows
    multiprocessing.freeze_support()
    
    app = EyeSaverApp()
    app.run()
