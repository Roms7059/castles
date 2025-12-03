import pygame
import json
import time
import math

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_DURATION = 900  # 15 minutes in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Difficulty settings (wave intervals in seconds)
DIFFICULTY_EASY = 120
DIFFICULTY_MEDIUM = 60
DIFFICULTY_HARD = 30

# Resource names
RESOURCES = ["exp", "or", "chair", "pain"]


class Entity:
    def __init__(self, x, y, health, speed, image=None):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.speed = speed
        self.image = image
        self.rect = None  # Define rect later based on image or dimensions

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def update(self):
        pass

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        elif self.rect:
            pygame.draw.rect(screen, RED, self.rect)  # Placeholder
        else:
            pygame.draw.circle(screen, RED, (self.x, self.y), 10)  # Even more basic placeholder


class Building(Entity):
    def __init__(self, x, y, health, image=None):
        super().__init__(x, y, health, 0, image)
        self.upgrades = {}

    def upgrade(self, upgrade_type):
        pass  # Implement upgrade logic


class Mob(Entity):
    def __init__(self, x, y, health, speed, damage, mob_type, image=None):
        super().__init__(x, y, health, speed, image)
        self.damage = damage
        self.mob_type = mob_type

    def attack(self, target):
        target.take_damage(self.damage)

    def update(self):
        # Basic movement towards the target (e.g., the building)
        pass


class Troop(Entity):
    def __init__(self, x, y, health, speed, damage, stamina, troop_type, image=None):
        super().__init__(x, y, health, speed, image)
        self.damage = damage
        self.stamina = stamina
        self.max_stamina = stamina
        self.troop_type = troop_type
        self.target = None

    def attack(self, target):
        if self.stamina > 0:
            target.take_damage(self.damage)
            self.stamina -= 1  # Example stamina usage
        else:
            print("Troop is too tired to attack!")

    def update(self):
        # Basic movement towards the target
        pass

    def consume_pain(self, amount):
      self.stamina = min(self.max_stamina, self.stamina + amount)


class Furnace(Building):
    def __init__(self, x, y, health=100, production_rate=10, storage_capacity=50, production_speed=1, image=None):
        super().__init__(x, y, health, image)
        self.production_rate = production_rate  # Pain per minute
        self.storage_capacity = storage_capacity
        self.current_pain = 0
        self.production_speed = production_speed # Time per pain
        self.last_production_time = time.time()
        self.upgrades = {
            "production_rate": 0,
            "storage_capacity": 0,
            "production_speed": 0,
            "health": 0
        }

    def update(self):
        current_time = time.time()
        if current_time - self.last_production_time >= self.production_speed:
            if self.current_pain < self.storage_capacity:
                self.current_pain += 1
                self.last_production_time = current_time

    def upgrade(self, upgrade_type):
        if upgrade_type == "production_rate":
            self.upgrades["production_rate"] += 1
            self.production_rate = self.production_rate * 1.1  # Example upgrade
        elif upgrade_type == "storage_capacity":
            self.upgrades["storage_capacity"] += 1
            self.storage_capacity = self.storage_capacity * 1.2
        elif upgrade_type == "production_speed":
            self.upgrades["production_speed"] += 1
            self.production_speed = self.production_speed * 0.9
        elif upgrade_type == "health":
            self.upgrades["health"] += 1
            self.max_health = self.max_health * 1.1
            self.health = self.max_health


class Wall(Building):
    def __init__(self, x, y, health=200, image=None):
        super().__init__(x, y, health, image)
        self.enchantments = [] # {type: "Thorns", level: 1}
        self.max_enchantments = 2
        self.upgrades = {
            "health": 0,
            "enchantment_slots": 0
        }

    def upgrade(self, upgrade_type):
        if upgrade_type == "health":
            self.upgrades["health"] += 1
            self.max_health = self.max_health * 1.1
            self.health = self.max_health
        elif upgrade_type == "enchantment_slots":
            if self.upgrades["enchantment_slots"] < self.max_enchantments:
                self.upgrades["enchantment_slots"] += 1
                self.max_enchantments += 1

    def add_enchantment(self, enchantment_type):
        if len(self.enchantments) < self.max_enchantments:
            self.enchantments.append({"type": enchantment_type, "level": 1})

    def activate_barrier(self, duration):
        # Activate a temporary barrier (implementation needed)
        pass


# Troop types
class Swordsman(Troop):
    def __init__(self, x, y):
        super().__init__(x, y, health=50, speed=3, damage=10, stamina=50, troop_type="swordsman")

class Archer(Troop):
    def __init__(self, x, y):
        super().__init__(x, y, health=30, speed=4, damage=15, stamina=30, troop_type="archer")

class Necromancer(Troop):
    def __init__(self, x, y):
        super().__init__(x, y, health=40, speed=2, damage=8, stamina=40, troop_type="necromancer")
        self.corpses = [] # List of dead mobs

    def summon_undead(self):
        if self.corpses:
            # Basic corpse summoning (implementation needed)
            corpse = self.corpses.pop()
            print("Necromancer summoned", corpse)
            return corpse # Returning the corpse
        else:
            print("No corpses available!")
            return None

class Assassin(Troop):
    def __init__(self, x, y):
        super().__init__(x, y, health=35, speed=5, damage=20, stamina=35, troop_type="assassin")

# Mob types
class Creep(Mob):
    def __init__(self, x, y, wave):
        base_health = 15
        base_force = 20
        health = base_health * (1 + 0.05 * (wave - 1))
        force = base_force * (1 + 0.04 * (wave - 1))
        super().__init__(x, y, health=health, speed=1, damage=force, mob_type="creep")

class Flyer(Mob):
    def __init__(self, x, y, wave):
        base_health = 15 / 1.10
        base_force = 20 * 1.2
        health = base_health * (1 + 0.05 * (wave - 1))
        force = base_force * (1 + 0.04 * (wave - 1))
        super().__init__(x, y, health=health, speed=2, damage=force, mob_type="flyer")

class Giant(Mob):
    def __init__(self, x, y, wave):
        base_health = 15 * 1.4
        base_force = 24 * 1.2
        health = base_health * (1 + 0.05 * (wave - 1))
        force = base_force * (1 + 0.04 * (wave - 1))

        super().__init__(x, y, health=health, speed=0.5, damage=force, mob_type="giant")

# Helper functions
def calculate_mob_stats(base_health, base_force, wave, health_multiplier=0.05, force_multiplier=0.04):
    health = base_health * (1 + health_multiplier * (wave - 1))
    force = base_force * (1 + force_multiplier * (wave - 1))
    return health, force

def generate_wave(wave_number, difficulty):
    mob_count = 20 + (wave_number - 1) * 12 # Linear scaling
    creep_ratio = 0.6
    flyer_ratio = 0.2
    giant_ratio = 0.2

    num_creeps = int(mob_count * creep_ratio)
    num_flyers = int(mob_count * flyer_ratio)
    num_giants = int(mob_count * giant_ratio)

    wave = []
    for _ in range(num_creeps):
        wave.append(Creep(800, 100, wave_number)) # Spawn at right edge
    for _ in range(num_flyers):
        wave.append(Flyer(800, 200, wave_number)) # Different y positions
    for _ in range(num_giants):
        wave.append(Giant(800, 300, wave_number)) # Different y positions
    return wave


# Game class
class Game:
    def __init__(self, difficulty):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Castles Defense")
        self.clock = pygame.time.Clock()
        self.difficulty = difficulty
        self.game_over = False
        self.game_time = 0
        self.wave_number = 0
        self.wave_start_time = 0
        self.resources = {"exp": 0, "or": 0, "chair": 0, "pain": 100}
        self.furnace = Furnace(100, HEIGHT // 2)
        self.wall = Wall(100, HEIGHT // 2 - 50)
        self.troops = []
        self.mobs = []
        self.load_data()

        if difficulty == "easy":
            self.wave_interval = DIFFICULTY_EASY
        elif difficulty == "medium":
            self.wave_interval = DIFFICULTY_MEDIUM
        else:
            self.wave_interval = DIFFICULTY_HARD

    def load_data(self):
        # Load persistent upgrades from JSON file (implementation needed)
        try:
            with open("save.json", "r") as f:
                save_data = json.load(f)
                # Apply loaded data to furnace, wall, etc.
                pass
        except FileNotFoundError:
            print("No save data found.")

    def save_data(self):
        # Save persistent upgrades to JSON file (implementation needed)
        save_data = {"furnace_upgrades": self.furnace.upgrades}
        with open("save.json", "w") as f:
            json.dump(save_data, f)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle clicks on upgrades, troops, etc.
                pass

    def update(self):
        if self.game_over:
            return

        self.game_time += 1 / FPS

        if self.game_time >= GAME_DURATION:
          if self.mobs:
            self.game_over = True
          else:
            self.game_over = True # Victory


        # Wave generation
        if self.game_time - self.wave_start_time >= self.wave_interval:
            self.wave_number += 1
            self.mobs = generate_wave(self.wave_number, self.difficulty)
            self.wave_start_time = self.game_time

        # Update game objects
        self.furnace.update()
        for troop in self.troops:
            troop.update()
            # Consume pain
            troop.consume_pain(self.furnace.production_rate / (FPS * 60))
        for mob in self.mobs:
            mob.update()
            # Basic mob movement
            mob.x -= mob.speed
            if mob.x < 150:
              mob.attack(self.wall) # Attack wall
              self.mobs.remove(mob)
        if not self.wall.is_alive():
          # Mobs attack furnace
          for mob in self.mobs:
            mob.attack(self.furnace)

        # Check for game over condition (furnace destroyed)
        if not self.furnace.is_alive():
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        # Draw game elements
        self.furnace.draw(self.screen)
        self.wall.draw(self.screen)
        for troop in self.troops:
            troop.draw(self.screen)
        for mob in self.mobs:
            mob.draw(self.screen)

        # Draw UI (resources, time, etc.)
        font = pygame.font.Font(None, 30)
        time_text = font.render(f"Time: {int(self.game_time)}", True, WHITE)
        self.screen.blit(time_text, (10, 10))

        resource_text = font.render(f"Resources: {self.resources}", True, WHITE)
        self.screen.blit(resource_text, (10, 40))

        health_text = font.render(f"Furnace Health: {self.furnace.health}", True, WHITE)
        self.screen.blit(health_text, (10, 70))

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # Game over screen
        print("Game Over!")
        self.save_data()
        pygame.quit()


if __name__ == "__main__":
    # Select difficulty
    difficulty = "medium"
    game = Game(difficulty)
    game.run()
