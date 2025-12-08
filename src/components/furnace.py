import time
from .building import Building

class Furnace(Building):
    def __init__(self, x, y, image=None, upgrades=None):
        base_health = 100
        
        if upgrades is None:
            upgrades = {"health": 0, "production_rate": 0, "storage_capacity": 0, "production_speed": 0}

        # Apply upgrades
        self.upgrades = upgrades
        health = base_health * (1.1 ** self.upgrades.get("health", 0))

        super().__init__(x, y, health, image)
        
        self.base_production_rate = 10
        self.base_storage_capacity = 50
        self.base_production_speed = 1

        prod_multiplier = 0.1
        cap_increment = 10

        self.production_rate = self.base_production_rate * (1.2 ** self.upgrades.get("production_rate", 0))
        self.storage_capacity = self.base_storage_capacity * (1.2 ** self.upgrades.get("storage_capacity", 0))
        self.production_speed = self.base_production_speed * (0.9 ** self.upgrades.get("production_speed", 0))

        self.current_pain = 0
        self.last_production_time = time.time()

    def update(self):
        current_time = time.time()
        if current_time - self.last_production_time >= self.production_speed:
            if self.current_pain < self.storage_capacity:
                self.current_pain += 1
                self.last_production_time = current_time