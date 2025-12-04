from .building import Building

class Wall(Building):
    def __init__(self, x, y, image=None, upgrades=None):
        base_health = 100
        
        if upgrades is None:
            upgrades = {"health": 0}

        # Apply upgrades
        self.upgrades = upgrades
        health = base_health * (1.1 ** self.upgrades.get("health", 0))

        super().__init__(x, y, health, image)
