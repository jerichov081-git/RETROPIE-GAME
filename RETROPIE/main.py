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
        pygame.display.set_caption("Pi Survivor - Balanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        
        # Player setup
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Timing and Waves
        self.start_time = pygame.time.get_ticks()
        self.spawn_timer = 0

    def get_current_wave(self):
        """Determines the current wave based on elapsed time."""
        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
        current_wave = WAVES[0]
        for wave in WAVES:
            if elapsed_seconds >= wave[0]:
                current_wave = wave
        return current_wave

    def spawn_logic(self, dt, wave_data):
        """Handles enemy spawning based on the current wave's rate."""
        self.spawn_timer += dt
        if self.spawn_timer >= wave_data[1]:
            # Spawn in a circle around the player
            angle = random.uniform(0, 360)
            spawn_pos = self.player.pos + pygame.math.Vector2(500, 0).rotate(angle)
            
            # Check if a boss should spawn (Boss wave and no boss currently alive)
            is_boss = wave_data[3] and not any(e.is_boss for e in self.enemies)
            
            enemy = Enemy(spawn_pos, self.player, wave_data[2], is_boss)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.spawn_timer = 0

    def level_up_menu(self):
        """Pauses the game and allows the player to choose a buff."""
        paused = True
        options = random.sample(list(UPGRADES.keys()), 3)
        
        while paused:
            self.screen.fill((30, 30, 40))
            title = self.font.render(f"LEVEL {self.player.level} REACHED!", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            for i, opt in enumerate(options):
                txt = f"{i+1}. {opt}: {UPGRADES[opt]['desc']}"
                surf = self.font.render(txt, True, XP_COLOR)
                rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 60))
                self.screen.blit(surf, rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        choice = options[int(event.unicode) - 1]
                        self.apply_upgrade(choice)
                        paused = False

    def apply_upgrade(self, choice):
        """Applies the selected buff to the player stats."""
        if choice == "Damage": 
            self.player.damage_mult += 0.5
        elif choice == "Fire Rate": 
            # Implement fire rate cooldown reduction if you have a fire timer
            pass 
        elif choice == "Health": 
            self.player.max_hp += 20
            self.player.hp = self.player.max_hp
        elif choice == "Projectiles": 
            self.player.projectile_count += 1
        elif choice == "Lifesteal":
            self.player.lifesteal += 0.05

    def draw_infinite_grid(self):
        """Draws a scrolling grid relative to player movement."""
        grid_size = 64
        offset_x = -int(self.player.pos.x % grid_size)
        offset_y = -int(self.player.pos.y % grid_size)
        
        for x in range(offset_x, SCREEN_WIDTH + grid_size, grid_size):
            pygame.draw.line(self.screen, (35, 35, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(offset_y, SCREEN_HEIGHT + grid_size, grid_size):
            pygame.draw.line(self.screen, (35, 35, 40), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        """The Main Game Loop."""
        while True:
            dt = self.clock.tick(FPS)
            current_wave = self.get_current_wave()
            
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Fire bullets with damage scaling
                        p = Projectile(self.player.pos, pygame.mouse.get_pos() + self.player.pos - pygame.math.Vector2(400, 300))
                        p.damage = 10 * self.player.damage_mult
                        self.projectiles.add(p); self.all_sprites.add(p)

            # 2. Spawning & Logic
            self.spawn_logic(dt, current_wave)
            self.player.get_input()
            self.all_sprites.update()

            # 3. Collision Handling
            # Projectiles vs Enemies
            for proj in self.projectiles:
                hits = pygame.sprite.spritecollide(proj, self.enemies, False)
                for enemy in hits:
                    enemy.hp -= proj.damage
                    proj.kill()
                    if enemy.hp <= 0:
                        # Lifesteal check
                        if random.random() < self.player.lifesteal:
                            self.player.hp = min(self.player.max_hp, self.player.hp + 5)
                        
                        # diverse drops: 10% health pack, 90% xp gem
                        drop_type = "health" if random.random() < 0.1 else "xp"
                        d = Drop(enemy.rect.center, drop_type)
                        self.drops.add(d); self.all_sprites.add(d)
                        enemy.kill()

            # Player vs Drops
            collected_drops = pygame.sprite.spritecollide(self.player, self.drops, True)
            for drop in collected_drops:
                if drop.type == "xp":
                    self.player.xp += 25
                    if self.player.xp >= self.player.xp_next_level:
                        self.player.level += 1
                        self.player.xp = 0
                        self.player.xp_next_level = int(self.player.xp_next_level * 1.2)
                        self.level_up_menu()
                elif drop.type == "health":
                    self.player.hp = min(self.player.max_hp, self.player.hp + 20)

            # Player vs Enemies (Damage)
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.player.hp -= 0.5
                if self.player.hp <= 0:
                    print("Game Over!")
                    pygame.quit(); sys.exit()

            # 4. Rendering
            self.screen.fill(DARK_GREY)
            self.draw_infinite_grid()
            
            # Camera offset drawing
            for sprite in self.all_sprites:
                screen_pos = sprite.pos - self.player.pos + pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                self.screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))
            
            self.player.draw_health(self.screen)
            
            # XP Bar UI
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 15))
            pygame.draw.rect(self.screen, XP_COLOR, (10, 10, (self.player.xp / self.player.xp_next_level) * 200, 15))
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
