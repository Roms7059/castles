import pygame
import random
from .components.furnace import Furnace
from .components.mob import Mob
from .components.wall import Wall
from .components.troop import Troop
from .utils import SaveManager
from .upgrade_menu import UpgradeMenu

# Définir la taille de la grille et des cellules
GRID_WIDTH = 8
GRID_HEIGHT = 8
GRID_SIZE = 100

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = GRID_WIDTH * GRID_SIZE
        self.screen_height = GRID_HEIGHT * GRID_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Castles")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'MENU'
        self.difficulty = 'Moyen'
        self.game_timer = 0
        self.wave_timer = 0
        self.pain_consumption_timer = 0
        self.wave_number = 0
        self.game_won = False
        self.time_limit = 15 * 60  # 15 minutes in seconds

        self.save_manager = SaveManager()
        self.save_data = self.save_manager.load_game()

        self.gold = self.save_data['currencies']['gold']
        self.exp = self.save_data['currencies']['exp']
        self.flesh = self.save_data['currencies']['flesh']

        self.furnace_upgrades = self.save_data['furnace_upgrades']
        self.wall_upgrades = self.save_data['wall_upgrades']
        self.troop_upgrades = self.save_data['troop_upgrades']

        self.upgrade_menu = UpgradeMenu(self)

        self._load_assets()

        # Boutons de difficulté
        self.font = pygame.font.Font(None, 50)
        self.easy_button_rect = pygame.Rect(self.screen_width / 2 - 150, self.screen_height / 2 - 50, 300, 70)
        self.medium_button_rect = pygame.Rect(self.screen_width / 2 - 150, self.screen_height / 2 + 50, 300, 70)
        self.hard_button_rect = pygame.Rect(self.screen_width / 2 - 150, self.screen_height / 2 + 150, 300, 70)
        self.upgrades_button_rect = pygame.Rect(self.screen_width / 2 - 150, self.screen_height / 2 + 250, 300, 70)
        self.back_to_menu_button_rect = pygame.Rect(self.screen_width / 2 - 150, self.screen_height / 2 + 100, 300, 70)
        self.button_color = (100, 100, 100)
        
        self.easy_text = self.font.render("Facile", True, (255, 255, 255))
        self.medium_text = self.font.render("Moyen", True, (255, 255, 255))
        self.hard_text = self.font.render("Difficile", True, (255, 255, 255))
        self.upgrades_text = self.font.render("Améliorations", True, (255, 255, 255))

        self.easy_text_rect = self.easy_text.get_rect(center=self.easy_button_rect.center)
        self.medium_text_rect = self.medium_text.get_rect(center=self.medium_button_rect.center)
        self.hard_text_rect = self.hard_text.get_rect(center=self.hard_button_rect.center)
        self.upgrades_text_rect = self.upgrades_text.get_rect(center=self.upgrades_button_rect.center)


        self.troop_stats = {
            'archer': {'health': 50, 'damage': 5, 'speed': 1, 'cost': 5, 'range': 200, 'cooldown': 1.0},
            'chevalier': {'health': 100, 'damage': 7, 'speed': 1, 'cost': 2, 'range': 50, 'cooldown': 0.8},
            'assassin': {'health': 70, 'damage': 10, 'speed': 2, 'cost': 10, 'range': 150, 'cooldown': 0.5}
        }

        # Objets du jeu
        self.game_objects = []
        self.troops = []
        self.furnace = None
        
    def _load_assets(self):
        # Assets du menu
        try:
            self.menu_furnace_image = pygame.image.load("src/assets/furnase.png").convert_alpha()
            self.menu_furnace_image = pygame.transform.scale(self.menu_furnace_image, (150, 150))
        except pygame.error as e:
            print(f"Impossible de charger l'image du menu: {e}")
            self.menu_furnace_image = None
            
        # Assets du jeu
        self.mob_images = {}
        self.troop_images = {}
        self.building_images = {}
        try:
            self.mob_images['rempant'] = pygame.image.load("src/assets/rempant.png").convert_alpha()
            self.mob_images['volant'] = pygame.image.load("src/assets/volent.png").convert_alpha()
            self.mob_images['geant'] = pygame.image.load("src/assets/geant.png").convert_alpha()
            
            self.troop_images['archer'] = pygame.image.load("src/assets/archer.png").convert_alpha()
            self.troop_images['chevalier'] = pygame.image.load("src/assets/chevalier.png").convert_alpha()
            self.troop_images['assassin'] = pygame.image.load("src/assets/assasin.png").convert_alpha()

            self.building_images['furnace'] = pygame.image.load("src/assets/furnase.png").convert_alpha()

            # Redimensionner les images
            self.mob_images['rempant'] = pygame.transform.scale(self.mob_images['rempant'], (50, 50))
            self.mob_images['volant'] = pygame.transform.scale(self.mob_images['volant'], (60, 60))
            self.mob_images['geant'] = pygame.transform.scale(self.mob_images['geant'], (100, 100))
            
            self.troop_images['archer'] = pygame.transform.scale(self.troop_images['archer'], (50, 50))
            self.troop_images['chevalier'] = pygame.transform.scale(self.troop_images['chevalier'], (50, 50))
            self.troop_images['assassin'] = pygame.transform.scale(self.troop_images['assassin'], (50, 50))

            self.building_images['furnace'] = pygame.transform.scale(self.building_images['furnace'], (100, 100))

        except pygame.error as e:
            print(f"Impossible de charger les images du jeu: {e}")


    def grid_to_pixels(self, grid_x, grid_y):
        pixel_x = grid_x * GRID_SIZE
        pixel_y = grid_y * GRID_SIZE
        return pixel_x, pixel_y

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.events()
            self.update(dt)
            self.draw()
        
        self.save_game()
        pygame.quit()

    def save_game(self):
        self.save_data['currencies']['gold'] = self.gold
        self.save_data['currencies']['exp'] = self.exp
        self.save_data['currencies']['flesh'] = self.flesh
        self.save_manager.save_game(self.save_data)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == 'PLAYING':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check if click is in menu area
                        if event.pos[1] > 6 * GRID_SIZE:
                            x_pos = event.pos[0]
                            if 0 < x_pos < 200:
                                self.spawn_troop('chevalier')
                            elif 200 < x_pos < 400:
                                self.spawn_troop('archer')
                            elif 400 < x_pos < 600:
                                self.spawn_troop('assassin')

            elif self.state == 'MENU':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.easy_button_rect.collidepoint(event.pos):
                            self.difficulty = 'Facile'
                            self.state = 'PLAYING'
                            self.start_game()
                        elif self.medium_button_rect.collidepoint(event.pos):
                            self.difficulty = 'Moyen'
                            self.state = 'PLAYING'
                            self.start_game()
                        elif self.hard_button_rect.collidepoint(event.pos):
                            self.difficulty = 'Difficile'
                            self.state = 'PLAYING'
                            self.start_game()
                        elif self.upgrades_button_rect.collidepoint(event.pos):
                            self.state = 'UPGRADE_MENU'
            
            elif self.state == 'UPGRADE_MENU':
                self.upgrade_menu.handle_event(event)
            elif self.state == 'GAME_OVER':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_to_menu_button_rect.collidepoint(event.pos):
                            self.state = 'MENU'

    def start_game(self):
        self.game_objects = []
        self.troops = []
        self.game_timer = 0
        self.wave_timer = 0
        self.wave_number = 0
        self.game_won = False

        # Placer la fournaise
        furnace_x, furnace_y = self.grid_to_pixels(1, 3)  # B5
        furnace_img = self.building_images.get('furnace')
        self.furnace = Furnace(x=furnace_x, y=furnace_y, image=furnace_img, upgrades=self.furnace_upgrades)
        self.game_objects.append(self.furnace)

        # Placer les remparts
        wall_positions = [
            (0, 2), (1, 2), (2, 2),  # A6, B6, C6
            (2, 3),                  # C5
            (0, 4), (1, 4), (2, 4)   # A4, B4, C4
        ]
        for pos in wall_positions:
            wall_x, wall_y = self.grid_to_pixels(pos[0], pos[1])
            wall = Wall(x=wall_x, y=wall_y, upgrades=self.wall_upgrades)
            self.game_objects.append(wall)

    def spawn_troop(self, troop_type):
        stats = self.troop_stats.get(troop_type)
        if not stats:
            print(f"Unknown troop type: {troop_type}")
            return

        if self.furnace.current_pain >= stats['cost']:
            self.furnace.current_pain -= stats['cost']
            
            strength_level = self.troop_upgrades['strength']
            stamina_level = self.troop_upgrades['stamina']

            damage = stats['damage'] * (1 + 0.58 * strength_level)
            health = stats['health'] * (1 + 0.45 * stamina_level)

            img = self.troop_images.get(troop_type)
            position = (self.furnace.rect.centerx, self.furnace.rect.centery)
            
            troop = Troop(x=position[0], y=position[1], 
                          health=health, speed=stats['speed'], 
                          damage=damage, troop_type=troop_type, 
                          attack_range=stats['range'], attack_cooldown=stats['cooldown'],
                          image=img)
            
            self.troops.append(troop)
            self.game_objects.append(troop)
        else:
            print(f"Not enough pain for {troop_type}. Need {stats['cost']}, have {self.furnace.current_pain}")

    def spawn_wave(self, wave_number):
        base_count_per_wave = 20
        growth_per_wave = 12
        total_mobs = base_count_per_wave + (wave_number - 1) * growth_per_wave

        if self.difficulty == 'Facile':
            total_mobs *= 0.5
        elif self.difficulty == 'Moyen':
            total_mobs *= 0.75

        rempant_ratio = 0.6
        volant_ratio = 0.2
        geant_ratio = 0.2

        wave_composition = {
            'rempant': int(total_mobs * rempant_ratio),
            'volant': int(total_mobs * volant_ratio),
            'geant': int(total_mobs * geant_ratio)
        }

        spawn_points_grid = [(7, 0), (7, 2), (7, 5)]  # H8, H6, H3
        spawn_points = [self.grid_to_pixels(gx, gy) for gx, gy in spawn_points_grid]

        base_rempant_hp = 15 * (1 + 0.05 * (wave_number - 1))
        base_rempant_force = 20 * (1 + 0.04 * (wave_number - 1))

        for mob_type, count in wave_composition.items():
            for _ in range(count):
                spawn_point = random.choice(spawn_points)
                
                if mob_type == 'rempant':
                    hp, force = base_rempant_hp, base_rempant_force
                elif mob_type == 'volant':
                    hp, force = base_rempant_hp / 1.10, base_rempant_force * 1.20
                elif mob_type == 'geant':
                    hp, force = base_rempant_hp * 1.40, (base_rempant_force * 1.20) * 1.20
                
                mob_img = self.mob_images.get(mob_type)
                mob = Mob(x=spawn_point[0], y=spawn_point[1], 
                            health=hp, speed=1, damage=force, 
                            mob_type=mob_type, target=self.furnace, image=mob_img)
                self.game_objects.append(mob)

    def update(self, dt):
        if self.state == 'PLAYING':
            self.game_timer += dt
            self.wave_timer += dt

            if not self.furnace.is_alive():
                self.game_won = False
                self.state = 'GAME_OVER'
                return

            if self.game_timer > self.time_limit:
                mobs = [obj for obj in self.game_objects if isinstance(obj, Mob) and obj.is_alive()]
                if not mobs:
                    self.game_won = True
                else:
                    self.game_won = False
                self.state = 'GAME_OVER'
                return

            wave_interval = 0
            if self.difficulty == 'Facile':
                wave_interval = 120
            elif self.difficulty == 'Moyen':
                wave_interval = 60
            elif self.difficulty == 'Difficile':
                wave_interval = 30

            if self.wave_number == 0:
                self.wave_number += 1
                self.spawn_wave(self.wave_number)
                self.wave_timer = 0

            if self.wave_timer > wave_interval:
                self.wave_timer = 0
                self.wave_number += 1
                self.spawn_wave(self.wave_number)

            if self.pain_consumption_timer > 1: # every second
                self.pain_consumption_timer = 0
                for troop in self.troops:
                    if self.furnace.current_pain >= troop.pain_consumption_rate:
                        self.furnace.current_pain -= troop.pain_consumption_rate
                        troop.has_pain = True
                    else:
                        troop.has_pain = False

            mobs = [obj for obj in self.game_objects if isinstance(obj, Mob)]
            troops = [obj for obj in self.game_objects if isinstance(obj, Troop)]

            # Update troops and handle their deaths
            dead_troops = []
            for troop in troops:
                troop.update(mobs)
                if not troop.is_alive():
                    dead_troops.append(troop)
            
            for troop in dead_troops:
                self.game_objects.remove(troop)
                self.troops.remove(troop)

            # Update mobs and handle their deaths
            dead_mobs = []
            for mob in mobs:
                mob.update(troops, self.furnace, mobs)
                if not mob.is_alive():
                    self.gold += mob.gold_reward
                    self.exp += mob.exp_reward
                    self.flesh += mob.flesh_reward
                    dead_mobs.append(mob)
            
            for mob in dead_mobs:
                self.game_objects.remove(mob)

            # Update other game objects
            for obj in self.game_objects:
                if not isinstance(obj, (Mob, Troop)):
                    obj.update()
            if self.state == 'UPGRADE_MENU':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # For now, just a back button
                        back_button_rect = pygame.Rect(10, 10, 150, 50)
                        if back_button_rect.collidepoint(event.pos):
                            self.state = 'MENU'

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.state == 'MENU':
            self.draw_menu()
        elif self.state == 'PLAYING':
            self.draw_game()
        elif self.state == 'GAME_OVER':
            self.draw_game_over()
        elif self.state == 'UPGRADE_MENU':
            self.upgrade_menu.draw(self.screen)

        pygame.display.flip()

    def draw_upgrade_menu(self):
        self.screen.fill((20, 20, 80))
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Améliorations", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, 100))
        self.screen.blit(title_text, title_rect)

        # Back button
        back_button_rect = pygame.Rect(10, 10, 150, 50)
        back_text = self.font.render("Retour", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        pygame.draw.rect(self.screen, self.button_color, back_button_rect, border_radius=15)
        self.screen.blit(back_text, back_text_rect)

    def draw_menu(self):
        self.screen.fill((20, 80, 20))
        if self.menu_furnace_image:
            img_rect = self.menu_furnace_image.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 200))
            self.screen.blit(self.menu_furnace_image, img_rect)
        
        pygame.draw.rect(self.screen, self.button_color, self.easy_button_rect, border_radius=15)
        self.screen.blit(self.easy_text, self.easy_text_rect)
        pygame.draw.rect(self.screen, self.button_color, self.medium_button_rect, border_radius=15)
        self.screen.blit(self.medium_text, self.medium_text_rect)
        pygame.draw.rect(self.screen, self.button_color, self.hard_button_rect, border_radius=15)
        self.screen.blit(self.hard_text, self.hard_text_rect)
        pygame.draw.rect(self.screen, self.button_color, self.upgrades_button_rect, border_radius=15)
        self.screen.blit(self.upgrades_text, self.upgrades_text_rect)

    def draw_game(self):
        self.screen.fill((20, 80, 20))
        
        # Dessiner la zone de menu
        menu_area_rect = pygame.Rect(0, 6 * GRID_SIZE, self.screen_width, 2 * GRID_SIZE)
        pygame.draw.rect(self.screen, (50, 50, 50), menu_area_rect)

        for obj in self.game_objects:
            obj.draw(self.screen)
            
        # Draw HUD
        hud_font = pygame.font.Font(None, 36)
        
        # Timer
        time_left = self.time_limit - self.game_timer
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        timer_text = hud_font.render(f'Temps restant: {minutes:02d}:{seconds:02d}', True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))

        # Wave number
        wave_text = hud_font.render(f'Vague: {self.wave_number}', True, (255, 255, 255))
        self.screen.blit(wave_text, (10, 40))

        # Mob count
        mobs_on_map = len([obj for obj in self.game_objects if isinstance(obj, Mob) and obj.is_alive()])
        mob_count_text = hud_font.render(f'Mobs: {mobs_on_map}', True, (255, 255, 255))
        self.screen.blit(mob_count_text, (self.screen_width - mob_count_text.get_width() - 10, 10))
        
        # Currencies in the bottom menu
        menu_y = 6 * GRID_SIZE + 10
        gold_text = hud_font.render(f'Or: {self.gold}', True, (255, 215, 0))
        self.screen.blit(gold_text, (10, menu_y))
        
        flesh_text = hud_font.render(f'Chair: {self.flesh}', True, (255, 100, 100))
        self.screen.blit(flesh_text, (200, menu_y))

        if self.furnace:
            pain_text = hud_font.render(f'Pain: {self.furnace.current_pain}', True, (200, 150, 100))
            self.screen.blit(pain_text, (400, menu_y))

        exp_text = hud_font.render(f'Exp: {self.exp}', True, (255, 255, 255))
        self.screen.blit(exp_text, (600, menu_y))

        # Troop spawn buttons
        menu_y_buttons = 7 * GRID_SIZE
        chevalier_text = hud_font.render(f'Chevalier', True, (255, 255, 255))
        self.screen.blit(chevalier_text, (10, menu_y_buttons))
        archer_text = hud_font.render(f'Archer', True, (255, 255, 255))
        self.screen.blit(archer_text, (210, menu_y_buttons))
        assassin_text = hud_font.render(f'Assassin', True, (255, 255, 255))
        self.screen.blit(assassin_text, (410, menu_y_buttons))

    def draw_game_over(self):
        self.screen.fill((20, 20, 20))
        game_over_font = pygame.font.Font(None, 100)
        if self.game_won:
            text = game_over_font.render("You Win!", True, (0, 255, 0))
        else:
            text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 100))
        self.screen.blit(text, text_rect)

        # Draw back to menu button
        back_text = self.font.render("Menu Principal", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_to_menu_button_rect.center)
        pygame.draw.rect(self.screen, self.button_color, self.back_to_menu_button_rect, border_radius=15)
        self.screen.blit(back_text, back_text_rect)

