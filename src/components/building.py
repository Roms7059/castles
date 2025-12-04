from .entity import Entity

class Building(Entity):
    def __init__(self, x, y, health, image=None):
        super().__init__(x, y, health, 0, image)
        self.upgrades = {}

    def upgrade(self, upgrade_type):
        pass  # Implement upgrade logic