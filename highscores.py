from __future__ import annotations
import os
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
# highscore.py
HIGHSCORE_FILE = "highscores.txt"

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        return [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        for score in highscores[:10]:
            f.write(f"{score}\n")

def draw_highscores(screen, highscores, font):
    title = font.render("High Scores", True, (255, 255, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
    for i, score in enumerate(highscores[:10]):
        score_text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 120 + i*30))