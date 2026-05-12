import pygame
import sys
import random
from settings import *
from entities import Player, Enemy, Drop
from weapons import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.start_time = pygame.time.get_ticks()
        self.spawn_timer = 0
        self.fire_cooldown = 0

    def get_current_wave(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        current = WAVES[0]
        for wave in WAVES:
            if elapsed >= wave[0]:
                current = wave
        return current

    def spawn_logic(self, dt, wave_data):
        self.spawn_timer += dt
        if self.spawn_timer >= wave_data[1]:
            angle = random.uniform(0, 360)
            spawn_pos = self.player.pos + pygame.math.Vector2(500, 0).rotate(angle)
            
            # If it's a boss wave and no boss exists, spawn one
            is_boss = wave_data[3] and not any(e.is_boss for e in self.enemies)
            enemy = Enemy(spawn_pos, self.player, wave_data[2], is_boss)
            
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.spawn_timer = 0

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            wave = self.get_current_wave()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            # Input & Auto-fire logic
            self.player.get_input()
            if pygame.mouse.get_pressed()[0]: # Left Click
                # Bullet Damage logic: Base 10 * multiplier
                p = Projectile(self.player.pos, pygame.mouse.get_pos() + self.player.pos - pygame.math.Vector2(400, 300))
                p.damage = 10 * self.player.damage_mult
                self.projectiles.add(p); self.all_sprites.add(p)

            # Wave Spawning
            self.spawn_logic(dt, wave)

            # Updates
            self.all_sprites.update()

            # Balanced Combat: Projectiles hit enemies but don't always kill
            for proj in self.projectiles:
                hits = pygame.sprite.spritecollide(proj, self.enemies, False)
                for enemy in hits:
                    enemy.hp -= proj.damage
                    proj.kill()
                    if enemy.hp <= 0:
                        # Diverse drops: 10% chance for Health, 90% for XP
                        drop_type = "health" if random.random() < 0.1 else "xp"
                        d = Drop(enemy.rect.center, drop_type)
                        self.drops.add(d); self.all_sprites.add(d)
                        enemy.kill()

            # UI & Rendering
            self.screen.fill(DARK_GREY)
            # (Insert Camera drawing logic here as per previous step)
            pygame.display.flip()
