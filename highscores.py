import os
import sys
import shutil
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def get_app_dir(): # This function returns the directory where the application is running.
    # Directory where the .exe or script is running
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir(): # This function returns the directory where the bundled data files are located.
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

def load_highscores(): # This function loads the high scores from the highscores.txt file.
    ensure_highscore_file()
    with open(HIGHSCORE_FILE, "r") as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]

def save_highscores(highscores): # This function saves the high scores to the highscores.txt file.
    with open(HIGHSCORE_FILE, "w") as f:
        for score in highscores[:10]:
            f.write(f"{score}\n")

def draw_highscores(screen, highscores, font): # This function draws the high scores on the screen.
    title = font.render("High Scores", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    for i, score in enumerate(highscores[:10]):
        score_text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 120 + i * 30))