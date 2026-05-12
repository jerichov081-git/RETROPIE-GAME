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

    def get_input(self):
        """Captures movement and dash input."""
        keys = pygame.key.get_pressed()
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

        if keys[pygame.K_SPACE] and not self.dashing:
            self.dashing = True
            self.dash_timer = DASH_DURATION

    def update(self):
        if self.dashing:
            dash_dir = self.vel.normalize() if self.vel.length() > 0 else pygame.math.Vector2(0,0)
            self.pos += dash_dir * DASH_SPEED
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.dashing = False
        else:
            self.pos += self.vel
        self.rect.center = self.pos

    def draw_health(self, screen):
        bar_width = 40
        bar_height = 6
        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = SCREEN_HEIGHT // 2 - 30
        fill = (max(0, self.hp) / self.max_hp) * bar_width
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, HEALTH_RED, (x, y, fill, bar_height))

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
