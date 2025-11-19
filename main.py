import multiprocessing
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from main import EyeSaverApp


def main():
    """Entry point for the eye-saver application."""
    # Multiprocessing support for Windows (prevents WinError 87)
    multiprocessing.freeze_support()
    
    app = EyeSaverApp()
    app.run()


if __name__ == "__main__":
    main()
