import unittest
from src.components.mob import Mob
from src.game import Game

class TestMobCreation(unittest.TestCase):

    def test_rempant_creation(self):
        base_rempant_hp = 15
        base_rempant_force = 20
        mob = Mob(x=0, y=0, health=base_rempant_hp, speed=1, damage=base_rempant_force, mob_type='rempant')
        self.assertEqual(mob.health, 15)
        self.assertEqual(mob.damage, 20)

    def test_volant_creation(self):
        base_rempant_hp = 15
        base_rempant_force = 20
        hp = base_rempant_hp / 1.10
        force = base_rempant_force * 1.20
        mob = Mob(x=0, y=0, health=hp, speed=1, damage=force, mob_type='volant')
        self.assertAlmostEqual(mob.health, 13.636, places=3)
        self.assertEqual(mob.damage, 24)

    def test_geant_creation(self):
        base_rempant_hp = 15
        base_rempant_force = 20
        hp = base_rempant_hp * 1.40
        force = (base_rempant_force * 1.20) * 1.20
        mob = Mob(x=0, y=0, health=hp, speed=1, damage=force, mob_type='geant')
        self.assertEqual(mob.health, 21)
        self.assertAlmostEqual(mob.damage, 28.8)

if __name__ == '__main__':
    unittest.main()