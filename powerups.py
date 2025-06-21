import pygame 
from random import random, choices, randint
from constants import *

def should_spawn_powerup(score):
    return score >= 20000 and random() < 0.08

def choose_powerup():
    types, weights = zip(*POWERUP_TYPES)
    return choices(types, weights)[0]

def spawn_powerup(score):
    if should_spawn_powerup(score):
        powerup_type = choose_powerup()
        x = randint(40, SCREEN_WIDTH-40)
        y = randint(40, SCREEN_HEIGHT-40)
        return PowerUp(powerup_type, (x, y))
    return None

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type, pos):
        super().__init__()
        self.type = powerup_type
        self.position = pygame.Vector2(pos)
        self.active = False
        self.timer = self.get_duration()
        self.collected = False
        self.cooldown = 6 if self.type == "nuke" else 0
        self.last_homing_time = 0
        self.icon = f"P^{POWERUP_DISPLAY_NAMES[self.type][0].upper()}"
        self.radius = 24

    def get_duration(self):
        if self.type == "double_points":
            return 15
        elif self.type == "rapid_fire":
            return 10
        elif self.type == "clone":
            return 5
        elif self.type == "homing_shot":
            return 25
        elif self.type == "shield":
            return 15  #15 seconds of invulnerability
        else:
            return 0  # nuke is collectable, single use

    def draw(self, screen):
        color = (0, 255, 255)
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius, 2)
        font = pygame.font.SysFont(None, 32)
        text = font.render(self.icon, True, color)
        screen.blit(text, (self.position.x - text.get_width()//2, self.position.y - text.get_height()//2))

    def activate(self, player, game_state, current_time):
        self.active = True
        if self.type == "double_points":
            game_state["score_multiplier"] = 2
        elif self.type == "nuke":
            game_state["nuke_count"] += 1
        elif self.type == "shield":
            player.invulnerable = True
            player.shield_timer = self.timer
            player.show_shield = True
        elif self.type == "rapid_fire":
            player.rapid_fire_timer = self.timer
        elif self.type == "clone":
            game_state["clone_timer"] = self.timer
            # spawn sidekick here
        elif self.type == "homing_shot":
            game_state["homing_shot_active"] = True
            self.last_homing_time = current_time

    def update(self, player, game_state, dt, current_time):
        if not self.active:
            return
        if self.type in ("double_points", "rapid_fire", "clone", "homing_shot", "shield"):
            self.timer -= dt
        if self.type == "homing_shot" and self.timer > 0:
            if current_time - self.last_homing_time >= 5:
                # player.fire_homing_shot()
                self.last_homing_time = current_time
        if self.type in ("double_points", "rapid_fire", "clone", "homing_shot", "shield") and self.timer <= 0:
            self.deactivate(player, game_state)

    def deactivate(self, player, game_state):
        self.active = False
        if self.type == "double_points":
            game_state["score_multiplier"] = 1
        elif self.type == "rapid_fire":
            player.rapid_fire_timer = 0
        elif self.type == "clone":
            game_state["clone_timer"] = 0
            # remove sidekick here
        elif self.type == "homing_shot":
            game_state["homing_shot_active"] = False
        elif self.type == "shield":
            player.invulnerable = False
            player.show_shield = False
    
    
    