import pygame
import math
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 24)).convert()
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2()
        self.hp = 100
        self.max_hp = 100
        self.xp = 0
        self.level = 1
        self.dashing = False
        self.dash_timer = 0

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED

        if keys[pygame.K_SPACE] and not self.dashing:
            self.dashing = True
            self.dash_timer = DASH_DURATION

    def update(self):
        if self.dashing:
            self.pos += self.vel.normalize() * DASH_SPEED if self.vel.length() > 0 else pygame.math.Vector2(0,0)
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.dashing = False
        else:
            self.pos += self.vel
        self.rect.center = self.pos

    def draw_health(self, screen):
        # Draw small bar over player
        width, height = 30, 5
        x, y = self.rect.centerx - width//2, self.rect.top - 10
        fill = (self.hp / self.max_hp) * width
        pygame.draw.rect(screen, (200, 0, 0), (x, y, fill, height))
