import os
import sys
import shutil

def get_app_dir():
    # Directory where the .exe or script is running
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir():
    # Directory where PyInstaller bundles data files
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

APP_DIR = get_app_dir()
DATA_DIR = get_data_dir()
HIGHSCORE_FILE = os.path.join(APP_DIR, "highscores.txt")
BUNDLED_HIGHSCORE = os.path.join(DATA_DIR, "highscores.txt")

def ensure_highscore_file():
    if not os.path.exists(HIGHSCORE_FILE):
        # Copy the default highscore file from bundled data
        shutil.copy(BUNDLED_HIGHSCORE, HIGHSCORE_FILE)

def load_highscores():
    ensure_highscore_file()
    with open(HIGHSCORE_FILE, "r") as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        for score in highscores[:10]:
            f.write(f"{score}\n")