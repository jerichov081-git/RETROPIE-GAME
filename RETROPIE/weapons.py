import pygame
import math
import random
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

class BaseballBat(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.image = pygame.Surface((60, 10), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.image, (150, 75, 0), (0, 0, 60, 10)) # Brown bat
        self.rect = self.image.get_rect()
        self.angle = 0
        self.damage = 15 * owner.damage_mult
        self.swinging = False

    def update(self):
        # Position the bat near the player
        self.rect.center = self.owner.pos
        if self.swinging:
            self.angle += 20
            if self.angle >= 360:
                self.angle = 0
                self.swinging = False
        
class SpinningBlade(Weapon):
    def __init__(self, owner, orbit_index):
        super().__init__(owner)
        self.image = pygame.Surface((30, 5)).convert()
        self.image.fill((200, 200, 200)) # Silver
        self.rect = self.image.get_rect()
        self.orbit_index = orbit_index
        self.angle = 0
        self.dist = 80
        self.damage = 10 * owner.damage_mult

    def update(self):
        self.angle += 0.1
        offset_angle = self.angle + (self.orbit_index * (2 * math.pi / 3))
        self.pos = self.owner.pos + pygame.math.Vector2(math.cos(offset_angle), math.sin(offset_angle)) * self.dist
        self.rect.center = self.pos

class Drone(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.image = pygame.Surface((15, 15)).convert()
        self.image.fill((0, 255, 255)) # Cyan
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(owner.pos)
        self.fire_timer = 0
        self.damage = 5

    def update(self):
        # Hover near player with a slight lag
        target = self.owner.pos + pygame.math.Vector2(-40, -40)
        self.pos += (target - self.pos) * 0.05
        self.rect.center = self.pos

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, damage=10, speed=10, color=(255, 255, 0)):
        super().__init__()
        self.image = pygame.Surface((8, 8)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.damage = damage
        
        direction = pygame.math.Vector2(target_pos) - pos
        if direction.length() > 0:
            self.vel = direction.normalize() * speed
        else:
            self.vel = pygame.math.Vector2(speed, 0)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        # Optimization: Kill if far from screen center
        if self.pos.distance_to(pygame.math.Vector2(400, 300)) > 1000:
            self.kill()
