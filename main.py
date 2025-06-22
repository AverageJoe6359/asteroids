import pygame # type: ignore
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
import sys
import os
from highscores import *
from gameover import *
from title_screen import *
from powerups import *
import time

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}") 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        main_menu(screen)
        paused = False
        score = 0
        next_extra_life_score = 10000
        pygame.display.set_caption("Asteroids")
        fps_clock = pygame.time.Clock()
        dt = 0
        updatable = pygame.sprite.Group() 
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        active_powerups = pygame.sprite.Group()
        active_effects = []
        sidekick = None
        game_state = {
            "score_multiplier": 1,
            "nuke_count": 0,
            "nuke_last_used": -999,
            "clone_timer": 0,
            "homing_shot_active": False
        }
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
        def draw_score(screen, score):
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH - 180, 10))
        asteroid_field = AsteroidField()
        def draw_nukes(screen, nuke_count):
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Nukes: {nuke_count}", True, (0, 255, 255))
            screen.blit(text, (10, 50))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    if event.key == pygame.K_b:
                        current_time = time.time()
                        if (
                            game_state["nuke_count"] > 0 and
                            current_time - game_state["nuke_last_used"] >= 6
                        ):
                            for a in list(asteroids):
                                a.kill()
                            game_state["nuke_count"] -= 1
                            game_state["nuke_last_used"] = current_time
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                        if sidekick:
                            sidekick.shoot()

            now = pygame.time.get_ticks()
            if not paused:
                dt = fps_clock.tick(60) / 1000
                updatable.update(dt)
                current_time = time.time()

                # --- SHIELD TIMER ---
                if player.invulnerable:
                    player.shield_timer -= dt
                    if player.shield_timer <= 0:
                        player.invulnerable = False
                        player.show_shield = False

                # --- RAPID FIRE TIMER ---
                if player.rapid_fire_timer > 0:
                    player.rapid_fire_timer -= dt
                    if player.rapid_fire_timer <= 0:
                        player.rapid_fire_timer = 0

                # --- CLONE (SIDEKICK) ---
                if game_state["clone_timer"] > 0:
                    game_state["clone_timer"] -= dt
                    if not sidekick:
                        sidekick = Player(player.position.x + 40, player.position.y + 40)
                        updatable.add(sidekick)
                        drawable.add(sidekick)
                else:
                    if sidekick:
                        sidekick.kill()
                        sidekick = None

                # --- MOVE SIDEKICK WITH PLAYER ---
                if sidekick:
                    sidekick.position = player.position + pygame.Vector2(40, 40)
                    sidekick.rotation = player.rotation

                # --- HOMING SHOT ---
                if game_state["homing_shot_active"]:
                    if not game_state["homing_shot_active"]:
                        game_state["homing_shot_timer"] = 0
                    game_state["homing_shot_timer"] += dt
                    if game_state["homing_shot_timer"] >= 3: 
                        if len(asteroids) > 0:
                            target = min(asteroids, key=lambda a: player.position.distance_to(a.position))
                            shot = Shot(player.position.x, player.position.y)
                            direction = (target.position - player.position).normalize()
                            shot.velocity = direction * PLAYER_SHOOT_SPEED
                        game_state["homing_shot_timer"] = 0
                else:
                    game_state["homing_shot_timer"] = 0

                 # --- POWERUP UPDATES & COLLECTION ---
                for powerup in list(active_powerups):
                    powerup.update(player, game_state, dt, current_time)
                    if player.check_collision(powerup):
                        powerup.activate(player, game_state, current_time)
                        powerup.collected = True
                        active_effects.append(powerup)  # Track effect after collection
                        powerup.kill()  # Remove from visible group
                
                # --- UPDATE ACTIVE EFFECTS (timed powerups) ---
                for effect in active_effects[:]:
                    effect.update(player, game_state, dt, current_time)
                    if not effect.active:
                        active_effects.remove(effect)
                # --- COLLISION DETECTION ---
                for a in asteroids:
                    if a.check_collision(player):
                        if not player_hit:
                            if not player.invulnerable:
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
                                score += 20 * game_state.get("score_multiplier", 1)
                            elif a.radius > 30:
                                score += 50 * game_state.get("score_multiplier", 1)
                            else:
                                score += 100 * game_state.get("score_multiplier", 1)
                            a.split()
                            s.kill()
                            powerup = spawn_powerup(score)
                            if (
                                powerup and
                                len(active_powerups) < 3 and
                                not any(p.type == powerup.type for p in active_powerups)
                            ):
                                active_powerups.add(powerup)

                # --- EXTRA LIFE ---
                if score >= next_extra_life_score:
                    lives += 1
                    next_extra_life_score += 10000

                # --- DRAW ---
                screen.fill("black")
                for d in drawable:
                    d.draw(screen)
                for powerup in active_powerups:
                    powerup.draw(screen)
                draw_lives(screen, lives)
                draw_score(screen, score)
                draw_nukes(screen, game_state["nuke_count"])            
                if paused:
                    font = pygame.font.SysFont(None, 72)
                    pause_text = font.render("Paused", True, (255, 255, 255))
                    screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - pause_text.get_height()//2))
                pygame.display.flip()

        game_over_screen(screen, score)

if __name__ == "__main__":
    main()