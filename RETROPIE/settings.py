import pygame

# Performance & Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 

# Colors
DARK_GREY = (20, 20, 25)
XP_COLOR = (50, 255, 50)
PLAYER_COLOR = (0, 200, 255)
ENEMY_RED = (255, 50, 50)
HEALTH_RED = (200, 30, 30)

# Game Balance
PLAYER_SPEED = 4
DASH_SPEED = 12
DASH_DURATION = 15 
SPAWN_RATE = 1000 

# Upgrade Data
UPGRADES = {
    "Speed": {"desc": "Move faster", "max": 5},
    "Fire Rate": {"desc": "Shoot faster", "max": 10},
    "Health": {"desc": "Increase Max HP", "max": 5},
    "Projectiles": {"desc": "+1 Bullet", "max": 3},
    "Damage": {"desc": "Hit harder", "max": 10}
}
