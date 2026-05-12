import pygame

# Performance & Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # Target 60, but Pi 3 may hover at 30-45 with high counts
TILE_SIZE = 32

# Colors
DARK_GREY = (20, 20, 25)
XP_COLOR = (50, 255, 50)
PLAYER_COLOR = (0, 200, 255)
ENEMY_RED = (255, 50, 50)

# Game Balance
PLAYER_SPEED = 4
DASH_SPEED = 12
DASH_DURATION = 15 # frames
SPAWN_RATE = 1000 # milliseconds