import pygame # type: ignore
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from highscores import load_highscores, save_highscores

def game_over_screen(screen, score):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    game_over_text = font.render("YOU DIED", True, (255, 0, 0))
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = small_font.render("Restart", True, (0, 0, 0))
    button_rect = pygame.Rect((SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 + 40, 150, 50))

    highscores = load_highscores()
    highscores.append(score)
    highscores = sorted(highscores, reverse=True)[:10]
    save_highscores(highscores)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Restart the game

        screen.fill("black")
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        screen.blit(restart_text, (button_rect.x + (button_rect.width - restart_text.get_width())//2,
                                   button_rect.y + (button_rect.height - restart_text.get_height())//2))
        pygame.display.flip()