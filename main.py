import pygame # type: ignore
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *
import sys


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}") 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    def draw_lives(screen, lives):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Lives: {lives}", True, (255, 0, 0))
        screen.blit(text, (10, 10))  
    asteroid_field = AsteroidField()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        now = pygame.time.get_ticks()
        updatable.update(dt)
        
        for a in asteroids:
            if a.check_collision(player):
                if not player_hit:
                    lives -= 1
                    player_hit = True
                    last_hit_time = now
            if player_hit and now - last_hit_time > hit_cooldown:
                player_hit = False 
                if lives == 0:       
                    sys.exit("Game Over!")
            for s in shots:
                if s.check_collision(a):
                    a.split()
                    s.kill()

                      
        screen.fill("black")
        for d in drawable:
            d.draw(screen)

        draw_lives(screen, lives)
        
        dt = (fps_clock.tick(60) / 1000)
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main()