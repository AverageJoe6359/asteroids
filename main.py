#imports
import pygame # type: ignore
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
import sys
import os
from highscores import * # Import the highscores functions
from gameover import * # Import the game_over_screen function
from title_screen import * # Import the main_menu function

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
        main_menu(screen)
        score = 0
        next_extra_life_score = 5000
        #Game initialization
        pygame.display.set_caption("Asteroids")
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
                            score += 20
                        elif a.radius > 30:
                            score += 50
                        else:
                            score += 100
                        a.split()
                        s.kill()
        #earn extra life
            if score >= next_extra_life_score:
                lives += 1
                next_extra_life_score += 5000
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