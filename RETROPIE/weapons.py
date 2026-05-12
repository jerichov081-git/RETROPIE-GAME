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
        # Brown rectangle for the bat
        self.image = pygame.Surface((40, 10)).convert()
        self.image.fill((150, 75, 0)) 
        self.rect = self.image.get_rect()
        self.base_image = self.image
        self.angle = 0
        self.damage = 15
        self.swinging = False

    def update(self):
        self.rect.center = self.owner.pos
        if self.swinging:
            self.angle += 15
            self.image = pygame.transform.rotate(self.base_image, self.angle)
            self.rect = self.image.get_rect(center=self.owner.pos)
            if self.angle >= 360:
                self.angle = 0
                self.swinging = False

class SpinningBlade(Weapon):
    def __init__(self, owner, index):
        super().__init__(owner)
        self.image = pygame.Surface((20, 5)).convert()
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.angle = 0
        self.index = index
        self.dist = 60
        self.damage = 10

    def update(self):
        self.angle += 0.05
        # Offset blades based on their index
        offset = self.angle + (self.index * (2 * math.pi / 3))
        self.rect.centerx = self.owner.pos.x + math.cos(offset) * self.dist
        self.rect.centery = self.owner.pos.y + math.sin(offset) * self.dist

class Drone(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.image = pygame.Surface((12, 12)).convert()
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(owner.pos)
        self.damage = 5

    def update(self):
        # Follow player with lag
        target = self.owner.pos + pygame.math.Vector2(-30, -30)
        self.pos += (target - self.pos) * 0.05
        self.rect.center = self.pos

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((8, 8)).convert()
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        direction = pygame.math.Vector2(target_pos) - pos
        self.vel = direction.normalize() * 10

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if not (0 <= self.pos.x <= SCREEN_WIDTH and 0 <= self.pos.y <= SCREEN_HEIGHT):
            self.kill()
