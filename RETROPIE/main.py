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
        pygame.display.set_caption("Pi Survivor")
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        
        # Player setup
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.spawn_timer = 0

    def spawn_enemy(self):
        # Spawn in a circle far enough away from the player
        angle = random.uniform(0, 360)
        dist = 500  # Distance from player
        spawn_pos = self.player.pos + pygame.math.Vector2(dist, 0).rotate(angle)
        
        enemy = Enemy(spawn_pos, self.player)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def level_up_menu(self):
        # Simple pause-state menu for upgrades
        paused = True
        # Randomly select 3 available upgrades from settings
        options = random.sample(list(UPGRADES.keys()), 3)
        
        while paused:
            self.screen.fill((30, 30, 40))
            title = self.font.render(f"LEVEL {self.player.level} REACHED!", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            rects = []
            for i, opt in enumerate(options):
                txt = f"{i+1}. {opt}: {UPGRADES[opt]['desc']}"
                surf = self.font.render(txt, True, XP_COLOR)
                rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 60))
                self.screen.blit(surf, rect)
                rects.append((rect, opt))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Check for 1, 2, or 3 keys
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        index = int(event.unicode) - 1
                        self.apply_upgrade(options[index])
                        paused = False

    def apply_upgrade(self, choice):
        if choice == "Speed": 
            self.player.speed += 0.5
        elif choice == "Fire Rate": 
            # Implement fire rate logic in weapons/player if needed
            pass
        elif choice == "Health": 
            self.player.max_hp += 20
            self.player.hp = self.player.max_hp
        elif choice == "Projectiles": 
            self.player.projectile_count += 1

    def draw_infinite_grid(self):
        # Draw grid lines offset by player position to simulate movement
        grid_size = 64
        offset_x = -int(self.player.pos.x % grid_size)
        offset_y = -int(self.player.pos.y % grid_size)
        
        for x in range(offset_x, SCREEN_WIDTH + grid_size, grid_size):
            pygame.draw.line(self.screen, (40, 40, 45), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(offset_y, SCREEN_HEIGHT + grid_size, grid_size):
            pygame.draw.line(self.screen, (40, 40, 45), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left Click
                        # Fire bullets relative to player screen position
                        p = Projectile(self.player.pos, pygame.mouse.get_pos() + self.player.pos - pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                        self.projectiles.add(p)
                        self.all_sprites.add(p)

            # 2. Spawning
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_RATE:
                self.spawn_enemy()
                self.spawn_timer = 0

            # 3. Logic & Physics
            self.player.get_input()
            self.all_sprites.update()

            # Bullet vs Enemy Collisions
            hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)
            for hit in hits:
                gem = ExperienceGem(hit.rect.center)
                self.gems.add(gem)
                self.all_sprites.add(gem)

            # Player vs Gem Collisions
            gem_hits = pygame.sprite.spritecollide(self.player, self.gems, True)
            for gem in gem_hits:
                self.player.xp += 25
                if self.player.xp >= self.player.xp_next_level:
                    self.player.level += 1
                    self.player.xp = 0
                    self.player.xp_next_level = int(self.player.xp_next_level * 1.2)
                    self.level_up_menu()

            # Enemy vs Player Damage
            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for enemy in enemy_hits:
                self.player.hp -= 0.5 
                if self.player.hp <= 0:
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()

            # 4. Rendering
            self.screen.fill(DARK_GREY)
            self.draw_infinite_grid()
            
            # Draw all sprites with camera offset
            for sprite in self.all_sprites:
                # Calculate screen position: (Sprite World Pos - Player World Pos + Screen Center)
                screen_pos = sprite.pos - self.player.pos + pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                self.screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))
            
            # UI: Health and XP
            self.player.draw_health(self.screen)
            
            # XP Bar at top
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 15))
            xp_ratio = min(self.player.xp / self.player.xp_next_level, 1.0)
            pygame.draw.rect(self.screen, XP_COLOR, (10, 10, xp_ratio * 200, 15))
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
