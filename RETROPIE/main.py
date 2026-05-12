import pygame
import sys
import random
from settings import *
from entities import Player, Enemy, ExperienceGem
from weapons import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.spawn_timer = 0
        self.camera_offset = pygame.math.Vector2(0, 0)

    def spawn_enemy(self):
        # Spawn outside screen relative to player
        angle = random.uniform(0, 360)
        dist = 500
        spawn_pos = self.player.pos + pygame.math.Vector2(dist, 0).rotate(angle)
        enemy = Enemy(spawn_pos, self.player)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def level_up_menu(self):
        # Simple pause and choose menu
        paused = True
        options = random.sample(list(UPGRADES.keys()), 3)
        
        while paused:
            self.screen.fill((30, 30, 40))
            title = self.font.render(f"LEVEL {self.player.level} REACHED!", True, (255,255,255))
            self.screen.blit(title, (SCREEN_WIDTH//2 - 100, 100))
            
            buttons = []
            for i, opt in enumerate(options):
                txt = f"{i+1}. {opt}: {UPGRADES[opt]['desc']}"
                surf = self.font.render(txt, True, XP_COLOR)
                rect = surf.get_rect(center=(SCREEN_WIDTH//2, 200 + i*60))
                self.screen.blit(surf, rect)
                buttons.append((rect, opt))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        choice = options[int(event.unicode)-1]
                        self.apply_upgrade(choice)
                        paused = False

    def apply_upgrade(self, choice):
        if choice == "Speed": self.player.bonus_speed += 0.5
        elif choice == "Fire Rate": self.player.fire_rate_mod += 50
        elif choice == "Health": 
            self.player.max_hp += 20
            self.player.hp += 20
        elif choice == "Projectiles": self.player.projectile_count += 1

    def draw_infinite_grid(self):
        # Draws a moving grid to simulate an infinite dungeon
        grid_size = 64
        offset_x = -int(self.player.pos.x % grid_size)
        offset_y = -int(self.player.pos.y % grid_size)
        
        for x in range(offset_x, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, (30, 30, 35), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(offset_y, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, (30, 30, 35), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Fire multiple projectiles based on upgrade
                    for i in range(self.player.projectile_count):
                        p = Projectile(self.player.pos, pygame.mouse.get_pos())
                        # Add slight spread for multiple bullets
                        if i > 0: p.vel.rotate_ip(random.randint(-10, 10))
                        self.projectiles.add(p); self.all_sprites.add(p)

            # Spawning
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_RATE:
                self.spawn_enemy(); self.spawn_timer = 0

            # Logic
            self.all_sprites.update()
            
            # Camera logic: We center the world on the player
            # Note: For the Pi 3, we move enemies relative to player
            
            # Collisions
            hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)
            for hit in hits:
                gem = ExperienceGem(hit.rect.center)
                self.gems.add(gem); self.all_sprites.add(gem)
                
            gem_hits = pygame.sprite.spritecollide(self.player, self.gems, True)
            for gem in gem_hits:
                self.player.xp += 25
                if self.player.xp >= self.player.xp_next_level:
                    self.player.level += 1
                    self.player.xp = 0
                    self.player.xp_next_level *= 1.2
                    self.level_up_menu()

            # Drawing
            self.screen.fill(DARK_GREY)
            self.draw_infinite_grid()
            
            # Draw everything relative to player (Simulated Camera)
            for sprite in self.all_sprites:
                screen_pos = sprite.pos - self.player.pos + pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                self.screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))
            
            # UI
            pygame.draw.rect(self.screen, (50,50,50), (10, 10, 200, 15))
            pygame.draw.rect(self.screen, XP_COLOR, (10, 10, (self.player.xp / self.player.xp_next_level) * 200, 15))
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
