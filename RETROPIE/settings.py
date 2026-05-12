import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 

# Colors
DARK_GREY = (20, 20, 25)
XP_COLOR = (50, 255, 50)
PLAYER_COLOR = (0, 200, 255)
ENEMY_RED = (255, 50, 50)
BOSS_PURPLE = (150, 0, 255)
HEALTH_RED = (200, 30, 30)

# Game Balance
PLAYER_SPEED = 4
DASH_SPEED = 12
DASH_DURATION = 15 

# WAVE SYSTEM: [Time in Seconds, Spawn Rate, Enemy Health, Is Boss Wave]
WAVES = [
    [0, 1500, 20, False],   # Wave 1: Easy, 20 HP
    [30, 1000, 40, False],  # Wave 2: Faster, 40 HP
    [60, 2000, 500, True],  # Wave 3: BOSS APPEARS
    [90, 800, 80, False],   # Wave 4: Swarm
]

UPGRADES = {
    "Damage": {"desc": "+50% DMG", "max": 10},
    "Fire Rate": {"desc": "-20% Cooldown", "max": 5},
    "Health": {"desc": "Heal & +20 Max HP", "max": 5},
    "Projectiles": {"desc": "+1 Bullet", "max": 3},
    "Lifesteal": {"desc": "5% Heal on Kill", "max": 3}
}
