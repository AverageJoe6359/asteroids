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
    asteroid_field = AsteroidField()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for a in asteroids:
            if a.check_collision(player):
                sys.exit("Game Over!")

                      
        screen.fill("black")
        for d in drawable:
            d.draw(screen)
       
        
        dt = (fps_clock.tick(60) / 1000)
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main()