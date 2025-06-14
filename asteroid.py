from circleshape import *
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "red", (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
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