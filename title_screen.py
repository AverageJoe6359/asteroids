from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from highscores import *
import pygame # type: ignore
import sys
def main_menu(screen): # This function displays the main menu of the game, allowing the player to start the game or view high scores.
    pygame.display.set_caption("Asteroids - Main Menu")
    screen.fill((0, 0, 30))  # Dark blue background
    pygame.display.flip()  # Update the display to show the background
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    play_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 60)
    highscores = load_highscores()

    while True: # Main loop for the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Start the game

        screen.fill((0, 0, 30))
        title = font.render("ASTEROIDS", True, (0, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        draw_highscores(screen, highscores, small_font)
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        play_text = small_font.render("Play", True, (0, 0, 0))
        screen.blit(play_text, (play_button.x + (play_button.width - play_text.get_width())//2,
                                play_button.y + (play_button.height - play_text.get_height())//2))
        pygame.display.flip()