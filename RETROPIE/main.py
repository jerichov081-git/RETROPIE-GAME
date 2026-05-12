import pygame
import sys
from settings import *
from entities import Player, Enemy
from weapons import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.spawn_timer = 0

    def spawn_enemy(self):
        # Spawn outside screen
        side = random.choice(['t', 'b', 'l', 'r'])
        if side == 't': pos = (random.randint(0, SCREEN_WIDTH), -20)
        elif side == 'b': pos = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT+20)
        elif side == 'l': pos = (-20, random.randint(0, SCREEN_HEIGHT))
        else: pos = (SCREEN_WIDTH+20, random.randint(0, SCREEN_HEIGHT))
        
        enemy = Enemy(pos, self.player)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left Click
                        p = Projectile(self.player.pos, pygame.mouse.get_pos())
                        self.projectiles.add(p)
                        self.all_sprites.add(p)

            # Spawning logic
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_RATE:
                self.spawn_enemy()
                self.spawn_timer = 0

            # Updates
            self.player.get_input()
            self.all_sprites.update()

            # Simple Collision (Projectiles vs Enemies)
            pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)

            # Draw
            self.screen.fill(DARK_GREY)
            self.all_sprites.draw(self.screen)
            
            # Mini-UI (XP Bar)
            pygame.draw.rect(self.screen, (50,50,50), (10, 10, 200, 20))
            pygame.draw.rect(self.screen, XP_COLOR, (10, 10, self.player.xp * 2, 20))
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()