import pygame
import sys
import random
from settings import *
from entities import Player, Enemy
from weapons import Projectile, BaseballBat, SpinningBlade, Drone

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player_weapons = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # START WITH BAT
        self.starter_weapon = BaseballBat(self.player)
        self.player_weapons.add(self.starter_weapon)
        self.all_sprites.add(self.starter_weapon)
        
        self.spawn_timer = 0

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Swing bat on click
                    self.starter_weapon.swinging = True

            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_RATE:
                # (Spawn logic remains same)
                side = random.choice(['t', 'b', 'l', 'r'])
                pos = (random.randint(0, SCREEN_WIDTH), -20) # Simplified for example
                enemy = Enemy(pos, self.player)
                self.enemies.add(enemy); self.all_sprites.add(enemy)
                self.spawn_timer = 0

            self.player.get_input()
            self.all_sprites.update()

            # COLLISION FOR ALL WEAPONS
            for weapon in self.player_weapons:
                hits = pygame.sprite.spritecollide(weapon, self.enemies, True)
                for hit in hits:
                    self.player.xp += 10 # Gain XP on kill

            self.screen.fill(DARK_GREY)
            self.all_sprites.draw(self.screen)
            self.player.draw_health(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
