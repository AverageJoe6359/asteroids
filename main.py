#imports
import pygame # type: ignore
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *
import sys

#game_over_screen function
def game_over_screen(screen, score):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = small_font.render("Restart", True, (0, 0, 0))
    button_rect = pygame.Rect((SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 + 40, 150, 50))

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

#main function
# This is the main entry point of the game.
# It initializes the game, sets up the screen, and starts the main game loop.
def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}") 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        fps_clock = pygame.time.Clock()
        dt = 0
        updatable = pygame.sprite.Group() 
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        AsteroidField.containers = (updatable, )
        Asteroid.containers = (asteroids, updatable, drawable)
        Player.containers = (updatable, drawable)
        Shot.containers = (updatable, drawable, shots)
        player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        lives = 3
        score = 0
        player_hit = False
        hit_cooldown = 1000  # milliseconds
        last_hit_time = 0
    #draw_lives and draw_score functions
        def draw_lives(screen, lives):
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Lives: {lives}", True, (255, 0, 0))
            screen.blit(text, (10, 10)) 
        def draw_score(screen, score):
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH - 180, 10))
        asteroid_field = AsteroidField()
    
    #game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
        #time handling and update
            now = pygame.time.get_ticks()
            updatable.update(dt)
        
        #collision detection
            for a in asteroids:
                if a.check_collision(player):
                    if not player_hit:
                        lives -= 1
                        player_hit = True
                        last_hit_time = now
                if player_hit and now - last_hit_time > hit_cooldown:
                    player_hit = False 
                if lives == 0:       
                    running = False
                for s in shots:
                    if s.check_collision(a):
                        if a.radius > 50:
                            score += 100
                        elif a.radius > 30:
                            score += 50
                        else:
                            score += 20
                        a.split()
                        s.kill()
        #earn extra life
            if score >= 5000:
                lives += 1
                score -= 5000
        #draw the game             
            screen.fill("black")
            for d in drawable:
                d.draw(screen)

            draw_lives(screen, lives)
            draw_score(screen, score)

            dt = (fps_clock.tick(60) / 1000)
        
            pygame.display.flip()
    
    # Show game over and wait for restart
        game_over_screen(screen, score)
        
if __name__ == "__main__":
    main()