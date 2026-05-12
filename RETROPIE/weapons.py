import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0)) # Yellow glow
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        
        # Calculate trajectory
        direction = pygame.math.Vector2(target_pos) - pos
        self.vel = direction.normalize() * 10

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        # Kill if off screen to save memory
        if not (0 <= self.pos.x <= SCREEN_WIDTH and 0 <= self.pos.y <= SCREEN_HEIGHT):
            self.kill()