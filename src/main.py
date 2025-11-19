from config_manager import ConfigManager
from dashboard_gui import DashboardGUI
import multiprocessing

class EyeSaverApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.dashboard_process = None
        
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
        # We need to communicate with the dashboard process or just launch it
        # Since we want a persistent dashboard that can minimize, we should probably run it in a separate process
        # that stays alive.
        
        if self.dashboard_process is None or not self.dashboard_process.is_alive():
            self.dashboard_process = multiprocessing.Process(target=self.run_dashboard_process)
            self.dashboard_process.start()
        else:
            # If already running, we can't easily bring it to front from here without IPC.
            # For simplicity in this version, we just let the user know or rely on them finding it in taskbar.
            # Or we can kill and restart (brute force).
            pass

    def run_dashboard_process(self):
        # Re-instantiate config manager in new process
        cm = ConfigManager()
        # We need a mock app controller or a way to communicate back.
        # For now, the dashboard will read/write config, but won't control the main app's pause state directly
        # unless we use shared memory or a file.
        # To keep it simple: Dashboard writes to config. Main app reads config.
        # Pause state: We can store 'paused' in config too?
        # Let's add 'paused' to config for IPC.
        
        # Mock app controller for simple callbacks that might not work across processes without IPC
        # So we will rely on ConfigManager for state sharing.
        
        gui = DashboardGUI(cm, None) 
        # We need to inject a way to control the main app.
        # Since we are in a different process, we can't pass 'self'.
        # We will modify DashboardGUI to use ConfigManager for pause state if we want that.
        # But for now, let's just show the stats and settings.
        # The 'Pause' button in Dashboard might not work for the background thread unless we sync.
        
        gui.show()

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
    import multiprocessing
    multiprocessing.freeze_support()
    
    app = EyeSaverApp()
    app.run()
