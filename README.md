# Eye Saver 👁️

![Version](https://img.shields.io/github/v/release/study8677/EyeSaver)
![License](https://img.shields.io/github/license/study8677/EyeSaver)
![Python](https://img.shields.io/badge/python-3.12-blue)

**Eye Saver** is a modern, lightweight Windows desktop application designed to protect your vision by reminding you to take breaks. Built with Python and CustomTkinter.

[中文文档](README_CN.md) | [Download](https://github.com/study8677/EyeSaver/releases)

## ✨ Features

- **Smart Reminders**: Automatically reminds you to rest every 50 minutes (customizable).
- **Modern Dashboard**: Beautiful, dark-mode compatible UI to track your focus sessions.
- **Statistics**: Track your daily and total rest counts.
- **Unobtrusive**: Runs in the system tray, minimal resource usage.
- **Sound Alerts**: Gentle audio cues when it's time to rest.

## 🚀 Installation

### Option 1: Download Executable (Recommended)
1. Go to the [Releases](https://github.com/study8677/EyeSaver/releases) page.
2. Download the latest `EyeSaver.exe`.
3. Run it directly!

### Option 2: Run from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/study8677/EyeSaver.git
   cd EyeSaver
   ```
2. Install dependencies using `uv` (or pip):
   ```bash
   uv sync
   ```
3. Run the application:
   ```bash
   uv run src/main.py
   ```

## 🛠️ Usage

1. **Start**: Run the application. The dashboard will open.
2. **Minimize**: Click the 'X' on the dashboard to minimize to the system tray.
3. **Control**: Right-click the tray icon to Pause/Resume or Open Dashboard.
4. **Settings**: Customize your work duration and sound preferences in the dashboard.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
