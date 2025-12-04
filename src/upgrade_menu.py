import pygame

class UpgradeMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)

    def draw(self, screen):
        screen.fill((20, 20, 80))
        
        # Title
        title_text = self.title_font.render("Améliorations", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.screen_width / 2, 50))
        screen.blit(title_text, title_rect)

        # Back button
        back_button_rect = pygame.Rect(10, 10, 150, 50)
        back_text = self.font.render("Retour", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        pygame.draw.rect(screen, (100, 100, 100), back_button_rect, border_radius=15)
        screen.blit(back_text, back_text_rect)

        # Display currencies
        gold_text = self.font.render(f'Or: {self.game.gold}', True, (255, 215, 0))
        screen.blit(gold_text, (self.game.screen_width - 200, 20))
        
        # Furnace Upgrades
        self.draw_furnace_upgrades(screen)

    def draw_furnace_upgrades(self, screen):
        furnace_title = self.font.render("Fournil", True, (255, 255, 255))
        screen.blit(furnace_title, (50, 150))
        
        # Health
        health_level = self.game.furnace_upgrades['health']
        health_cost = int(100 * 1.5**health_level)
        health_text = self.font.render(f"Vie (Lvl {health_level}): {health_cost} Or", True, (255, 255, 255))
        screen.blit(health_text, (50, 200))
        
        # Production Rate
        prod_level = self.game.furnace_upgrades['production_rate']
        prod_cost = int(100 * 1.5**prod_level)
        prod_text = self.font.render(f"Production (Lvl {prod_level}): {prod_cost} Or", True, (255, 255, 255))
        screen.blit(prod_text, (50, 250))

        # Storage Capacity
        cap_level = self.game.furnace_upgrades['storage_capacity']
        cap_cost = int(100 * 1.5**cap_level)
        cap_text = self.font.render(f"Capacité (Lvl {cap_level}): {cap_cost} Or", True, (255, 255, 255))
        screen.blit(cap_text, (50, 300))

        # Production Speed
        speed_level = self.game.furnace_upgrades['production_speed']
        speed_cost = int(100 * 1.5**speed_level)
        speed_text = self.font.render(f"Vitesse (Lvl {speed_level}): {speed_cost} Or", True, (255, 255, 255))
        screen.blit(speed_text, (50, 350))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Back button
                back_button_rect = pygame.Rect(10, 10, 150, 50)
                if back_button_rect.collidepoint(event.pos):
                    self.game.state = 'MENU'
                
                # Furnace upgrade buttons (simplified rects for now)
                if pygame.Rect(50, 200, 400, 40).collidepoint(event.pos):
                    self.upgrade_furnace('health')
                if pygame.Rect(50, 250, 400, 40).collidepoint(event.pos):
                    self.upgrade_furnace('production_rate')
                if pygame.Rect(50, 300, 400, 40).collidepoint(event.pos):
                    self.upgrade_furnace('storage_capacity')
                if pygame.Rect(50, 350, 400, 40).collidepoint(event.pos):
                    self.upgrade_furnace('production_speed')

    def upgrade_furnace(self, upgrade_type):
        level = self.game.furnace_upgrades[upgrade_type]
        cost = int(100 * 1.5**level)

        if self.game.gold >= cost:
            self.game.gold -= cost
            self.game.furnace_upgrades[upgrade_type] += 1
            self.game.save_game()
