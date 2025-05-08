import sys
import json
from PyQt5.QtWidgets import QApplication
from ui.startup_window import StartupWindow

CONFIG_PATH = 'config.json'

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default = {"username": "User", "port": 5000, "theme": "XP"}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default, f, indent=4)
        return default

if __name__ == '__main__':
    config = load_config()
    app = QApplication(sys.argv)
    startup = StartupWindow(config)
    startup.show()
    sys.exit(app.exec_())