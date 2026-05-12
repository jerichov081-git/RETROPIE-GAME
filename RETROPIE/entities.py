import pygame
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
        
        # Stats
        self.max_hp = 100
        self.hp = 100
        self.speed = PLAYER_SPEED
        self.damage_mult = 1.0
        self.lifesteal = 0
        self.xp = 0
        self.xp_next_level = 100
        self.level = 1
        self.projectile_count = 1
        
        self.dashing = False
        self.dash_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        current_speed = DASH_SPEED if self.dashing else self.speed
        if self.vel.length() > 0:
            self.pos += self.vel.normalize() * current_speed
        
        if self.dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.dashing = False
            
        self.rect.center = self.pos

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, target, hp, is_boss=False):
        super().__init__()
        size = (48, 48) if is_boss else (20, 20)
        self.image = pygame.Surface(size).convert()
        self.image.fill(BOSS_PURPLE if is_boss else ENEMY_RED)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.target = target
        self.hp = hp
        self.is_boss = is_boss
        self.speed = random.uniform(1.0, 1.8) if not is_boss else 1.2

    def update(self):
        dir = (self.target.pos - self.pos)
        if dir.length() > 0:
            self.pos += dir.normalize() * self.speed
        self.rect.center = self.pos

class Drop(pygame.sprite.Sprite):
    def __init__(self, pos, type="xp"):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((8, 8)).convert()
        self.image.fill(XP_COLOR if type == "xp" else HEALTH_RED)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
