# Constants for the Asteroids game
# These constants define various parameters for the game, such as screen dimensions, asteroid properties, player
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3 #seconds

SHOT_RADIUS = 5

# Power-up types and their probabilities
POWERUP_TYPES = [
    ("double_points", 0.125),  # 12.5% chance
    ("nuke", 0.125),           # 12.5% chance
    ("shield", 0.20),          # 20% chance
    ("rapid_fire", 0.20),      # 20% chance
    ("clone", 0.15),           # 15% chance
    ("homing_shot", 0.20)      # 20% chance
]

# Power-up display names
POWERUP_DISPLAY_NAMES = {
    "double_points": "Double Points",
    "nuke": "Nuke",
    "shield": "Shield",
    "rapid_fire": "Rapid Fire",
    "clone": "Clone",
    "homing_shot": "Homing Shot"
}