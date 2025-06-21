#imports
from circleshape import *
from constants import *
from shot import *
from powerups import *
#player class
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable = False
        self.show_shield = False
        self.shield_timer = 0
        self.rapid_fire_timer = 0
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "blue", self.triangle(), 2)
        if hasattr(self, "show_shield") and self.show_shield:
            pygame.draw.circle(screen, (0,255,255), (int(self.position.x), int(self.position.y)), self.radius+10, 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    #player update method
    # This method updates the player's position and handles shooting.
    def update(self, dt):
        self.shoot_timer = max(0, self.shoot_timer - dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        

    def shoot(self):
        if self.rapid_fire_timer > 0:
            cooldown = PLAYER_SHOOT_COOLDOWN / 3  # 3x faster, adjust as needed
        else:
            cooldown = PLAYER_SHOOT_COOLDOWN
        if self.shoot_timer > 0:
            return
        self.shoot_timer = cooldown

        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

  