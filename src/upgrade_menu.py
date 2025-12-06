import pygame

class UpgradeMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)
        self.upgrade_max_levels = {
            'health': 10,
            'production_rate': 10,
            'storage_capacity': 10,
            'production_speed': 10,
            'strength': 100,
            'stamina': 100
        }
        self.buy_button_rects = {}

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
        # Troop Upgrades
        self.draw_troop_upgrades(screen)


    def draw_furnace_upgrades(self, screen):
        furnace_title = self.font.render("Fournil", True, (255, 255, 255))
        screen.blit(furnace_title, (50, 150))

        upgrades = {
            'health': "Vie",
            'production_rate': "Production",
            'storage_capacity': "Capacité",
            'production_speed': "Vitesse"
        }

        base_values = {
            'health': 100,
            'production_rate': 10,
            'storage_capacity': 50,
            'production_speed': 1
        }

        y_offset = 200
        for upgrade_type, upgrade_name in upgrades.items():
            level = self.game.furnace_upgrades[upgrade_type]
            max_level = self.upgrade_max_levels[upgrade_type]
            cost = int(100 * 1.5**level)

            # Draw border
            border_rect = pygame.Rect(40, y_offset - 10, self.game.screen_width - 80, 60)
            pygame.draw.rect(screen, (150, 150, 150), border_rect, 2, border_radius=10)

            # Upgrade name
            name_text = self.font.render(upgrade_name, True, (255, 255, 255))
            screen.blit(name_text, (50, y_offset))

            # Level counter
            level_text = self.font.render(f"Lvl {level}/{max_level}", True, (255, 255, 255))
            screen.blit(level_text, (300, y_offset))
            
            # Upgrade value
            base_value = base_values[upgrade_type]
            if upgrade_type == 'health':
                current_value = base_value * (1.1 ** level)
                next_value = base_value * (1.1 ** (level + 1))
                value_text = f"{current_value:.0f} -> {next_value:.0f}"
            elif upgrade_type == 'production_rate':
                current_value = base_value * (1.2 ** level)
                next_value = base_value * (1.2 ** (level + 1))
                value_text = f"{current_value:.2f}/s -> {next_value:.2f}/s"
            elif upgrade_type == 'storage_capacity':
                current_value = base_value * (1.2 ** level)
                next_value = base_value * (1.2 ** (level + 1))
                value_text = f"{current_value:.0f} -> {next_value:.0f}"
            elif upgrade_type == 'production_speed':
                current_value = base_value * (0.9 ** level)
                next_value = base_value * (0.9 ** (level + 1))
                value_text = f"{current_value:.2f}s -> {next_value:.2f}s"
            
            value_surface = self.font.render(value_text, True, (255, 255, 255))
            screen.blit(value_surface, (50, y_offset + 30))

            # Buy button
            buy_button_rect = pygame.Rect(self.game.screen_width - 250, y_offset - 5, 200, 50)
            self.buy_button_rects[upgrade_type] = buy_button_rect
            
            if level < max_level:
                pygame.draw.rect(screen, (0, 150, 0), buy_button_rect, border_radius=10)
                cost_text = self.font.render(f"Acheter ({cost} Or)", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (100, 100, 100), buy_button_rect, border_radius=10)
                cost_text = self.font.render("Max", True, (255, 255, 255))
                
            cost_text_rect = cost_text.get_rect(center=buy_button_rect.center)
            screen.blit(cost_text, cost_text_rect)

            y_offset += 70

    def draw_troop_upgrades(self, screen):
        troop_title = self.font.render("Troupes", True, (255, 255, 255))
        screen.blit(troop_title, (50, 450))

        upgrades = {
            'strength': "Force",
            'stamina': "Endurance",
        }

        base_values = {
            'strength': 1,
            'stamina': 1,
        }

        y_offset = 500
        for upgrade_type, upgrade_name in upgrades.items():
            level = self.game.troop_upgrades[upgrade_type]
            max_level = self.upgrade_max_levels[upgrade_type]
            cost = int(10 * 1.2**level)

            # Draw border
            border_rect = pygame.Rect(40, y_offset - 10, self.game.screen_width - 80, 60)
            pygame.draw.rect(screen, (150, 150, 150), border_rect, 2, border_radius=10)

            # Upgrade name
            name_text = self.font.render(upgrade_name, True, (255, 255, 255))
            screen.blit(name_text, (50, y_offset))

            # Level counter
            level_text = self.font.render(f"Lvl {level}/{max_level}", True, (255, 255, 255))
            screen.blit(level_text, (300, y_offset))

            # Upgrade value
            base_value = base_values[upgrade_type]
            if upgrade_type == 'strength':
                current_value = 1 + 0.05 * level
                next_value = 1 + 0.05 * (level + 1)
                value_text = f"x{current_value:.2f} -> x{next_value:.2f}"
            elif upgrade_type == 'stamina':
                current_value = 1 + 0.05 * level
                next_value = 1 + 0.05 * (level + 1)
                value_text = f"x{current_value:.2f} -> x{next_value:.2f}"

            value_surface = self.font.render(value_text, True, (255, 255, 255))
            screen.blit(value_surface, (50, y_offset + 30))
            
            # Buy button
            buy_button_rect = pygame.Rect(self.game.screen_width - 250, y_offset - 5, 200, 50)
            self.buy_button_rects[upgrade_type] = buy_button_rect
            
            if level < max_level:
                pygame.draw.rect(screen, (0, 150, 0), buy_button_rect, border_radius=10)
                cost_text = self.font.render(f"Acheter ({cost} Or)", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (100, 100, 100), buy_button_rect, border_radius=10)
                cost_text = self.font.render("Max", True, (255, 255, 255))
                
            cost_text_rect = cost_text.get_rect(center=buy_button_rect.center)
            screen.blit(cost_text, cost_text_rect)

            y_offset += 70


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Back button
                back_button_rect = pygame.Rect(10, 10, 150, 50)
                if back_button_rect.collidepoint(event.pos):
                    self.game.state = 'MENU'
                
                # Furnace and troop upgrade buttons
                for upgrade_type, rect in self.buy_button_rects.items():
                    if rect.collidepoint(event.pos):
                        if upgrade_type in self.game.furnace_upgrades:
                            self.upgrade_furnace(upgrade_type)
                        elif upgrade_type in self.game.troop_upgrades:
                            self.upgrade_troop(upgrade_type)


    def upgrade_furnace(self, upgrade_type):
        level = self.game.furnace_upgrades[upgrade_type]
        max_level = self.upgrade_max_levels[upgrade_type]
        cost = int(100 * 1.5**level)

        if level < max_level and self.game.gold >= cost:
            self.game.gold -= cost
            self.game.furnace_upgrades[upgrade_type] += 1
            self.game.save_game()

    def upgrade_troop(self, upgrade_type):
        level = self.game.troop_upgrades[upgrade_type]
        max_level = self.upgrade_max_levels[upgrade_type]
        cost = int(10 * 1.2**level)

        if level < max_level and self.game.gold >= cost:
            self.game.gold -= cost
            self.game.troop_upgrades[upgrade_type] += 1
            self.game.save_game()
