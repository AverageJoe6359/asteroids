from circleshape import *
from constants import *
import random

def get_asteroid_color(radius): # This function returns a color based on the asteroid's radius.
    if radius > 50:
        return (255, 0, 0)      # Red for large asteroids
    elif radius > 30:
        return (255, 165, 0)    # Orange for medium asteroids
    else:
        return (255, 255, 0)  # Yellow for small asteroids

class Asteroid(CircleShape): # This class represents an asteroid in the Asteroids game, inheriting from CircleShape.
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen): # This method draws the asteroid on the screen with a color based on its radius.
        color = get_asteroid_color(self.radius)
        pygame.draw.circle(screen, color, (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt): # This method updates the asteroid's position based on its velocity and the elapsed time.
        self.position += (self.velocity * dt)

    def split(self): # This method handles the splitting of the asteroid into two smaller asteroids when it is destroyed.
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        rand_angle = random.uniform(20, 50)
        new_1 = self.velocity.rotate(rand_angle)
        new_2 = self.velocity.rotate(-rand_angle)
        new_rad = self.radius - ASTEROID_MIN_RADIUS
        split_ast_1 = Asteroid(self.position.x, self.position.y, new_rad)
        split_ast_2 = Asteroid(self.position.x, self.position.y, new_rad)
        split_ast_1.velocity = new_1 * 1.2
        split_ast_2.velocity = new_2 * 1.2