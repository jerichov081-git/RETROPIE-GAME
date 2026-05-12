import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Use .convert() for better Pi 3 performance
        self.image = pygame.Surface((24, 24)).convert() 
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # Movement and Stats
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        
        # Health System
        self.max_hp = 100
        self.hp = 100
        
        # XP and Levels
        self.xp = 0
        self.level = 1
        
        # Dash state
        self.dashing = False
        self.dash_timer = 0

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

        if keys[pygame.K_SPACE] and not self.dashing:
            self.dashing = True
            self.dash_timer = DASH_DURATION

    def update(self):
        # Update position based on velocity
        if self.dashing:
            dash_dir = self.vel.normalize() if self.vel.length() > 0 else pygame.math.Vector2(0,0)
            self.pos += dash_dir * DASH_SPEED
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.dashing = False
        else:
            self.pos += self.vel
        
        # This keeps the 'rect' updated for collision detection
        self.rect.center = self.pos

    def draw_health(self, screen):
        # Draw health bar above player's head
        bar_width = 30
        bar_height = 5
        # Center the bar over the screen center (since player is always centered)
        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = SCREEN_HEIGHT // 2 - 25
        
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        
        pygame.draw.rect(screen, (50, 50, 50), outline_rect)
        pygame.draw.rect(screen, HEALTH_RED, fill_rect)
