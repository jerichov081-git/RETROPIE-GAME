# Inside the run() loop of main.py, under the Logic/Updates section:

# 1. Check for enemy collision with player
enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
for enemy in enemy_hits:
    self.player.hp -= 0.5 # Damage per frame while touching
    if self.player.hp <= 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()

# 2. In the Drawing section:
self.screen.fill(DARK_GREY)
self.draw_infinite_grid() #

# Draw all sprites relative to the player's position (Camera)
for sprite in self.all_sprites:
    # Calculate where the sprite should be on screen relative to the player
    screen_pos = sprite.pos - self.player.pos + pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    self.screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))

# Draw player health bar last so it is on top
self.player.draw_health(self.screen)
