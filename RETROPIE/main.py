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

    def get_current_wave(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        current = WAVES[0]
        for wave in WAVES:
            if elapsed >= wave[0]: current = wave
        return current

    def spawn_logic(self, dt, wave_data):
        self.spawn_timer += dt
        if self.spawn_timer >= wave_data[1]:
            angle = random.uniform(0, 360)
            spawn_pos = self.player.pos + pygame.math.Vector2(500, 0).rotate(angle)
            is_boss = wave_data[3] and not any(e.is_boss for e in self.enemies)
            enemy = Enemy(spawn_pos, self.player, wave_data[2], is_boss)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.spawn_timer = 0

    def level_up_menu(self):
        paused = True
        options = random.sample(list(UPGRADES.keys()), 3)
        while paused:
            self.screen.fill((30, 30, 40))
            title = self.font.render(f"LEVEL {self.player.level} REACHED!", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            for i, opt in enumerate(options):
                txt = f"{i+1}. {opt}: {UPGRADES[opt]['desc']}"
                surf = self.font.render(txt, True, XP_COLOR)
                self.screen.blit(surf, (SCREEN_WIDTH // 2 - 100, 250 + i * 60))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    self.apply_upgrade(options[int(event.unicode)-1])
                    paused = False

    def apply_upgrade(self, choice):
        if choice == "Damage": self.player.damage_mult += 0.5
        elif choice == "Health":
            self.player.max_hp += 20
            self.player.hp = self.player.max_hp
        elif choice == "Projectiles": self.player.projectile_count += 1
        elif choice == "Lifesteal": self.player.lifesteal += 0.05

    def draw_infinite_grid(self):
        grid_size = 64
        offset_x = -int(self.player.pos.x % grid_size)
        offset_y = -int(self.player.pos.y % grid_size)
        for x in range(offset_x, SCREEN_WIDTH + grid_size, grid_size):
            pygame.draw.line(self.screen, (35, 35, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(offset_y, SCREEN_HEIGHT + grid_size, grid_size):
            pygame.draw.line(self.screen, (35, 35, 40), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            wave = self.get_current_wave()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    p = Projectile(self.player.pos, pygame.mouse.get_pos() + self.player.pos - pygame.math.Vector2(400, 300))
                    p.damage = 10 * self.player.damage_mult
                    self.projectiles.add(p); self.all_sprites.add(p)

            self.spawn_logic(dt, wave)
            self.player.get_input()
            self.all_sprites.update()

            # Combat logic with enemy health
            for proj in self.projectiles:
                hits = pygame.sprite.spritecollide(proj, self.enemies, False)
                for enemy in hits:
                    enemy.hp -= proj.damage
                    proj.kill()
                    if enemy.hp <= 0:
                        if random.random() < self.player.lifesteal:
                            self.player.hp = min(self.player.max_hp, self.player.hp + 5)
                        drop_type = "health" if random.random() < 0.1 else "xp"
                        d = Drop(enemy.rect.center, drop_type)
                        self.drops.add(d); self.all_sprites.add(d)
                        enemy.kill()

            # Item Collection
            collected = pygame.sprite.spritecollide(self.player, self.drops, True)
            for drop in collected:
                if drop.type == "xp":
                    self.player.xp += 25
                    if self.player.xp >= self.player.xp_next_level:
                        self.player.level += 1
                        self.player.xp = 0
                        self.player.xp_next_level = int(self.player.xp_next_level * 1.2)
                        self.level_up_menu()
                else: self.player.hp = min(self.player.max_hp, self.player.hp + 20)

            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.player.hp -= 0.5
                if self.player.hp <= 0: pygame.quit(); sys.exit()

            self.screen.fill(DARK_GREY)
            self.draw_infinite_grid()
            for sprite in self.all_sprites:
                screen_pos = sprite.pos - self.player.pos + pygame.math.Vector2(400, 300)
                self.screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))
            self.player.draw_health(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
