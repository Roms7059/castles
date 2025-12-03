import unittest
from src.main import calculate_mob_stats, Game, Creep, Flyer, Giant

class TestCalculations(unittest.TestCase):

    def test_mob_stats_wave_1(self):
        base_health = 15
        base_force = 20
        health, force = calculate_mob_stats(base_health, base_force, 1)
        self.assertAlmostEqual(health, 15)
        self.assertAlmostEqual(force, 20)

    def test_mob_stats_wave_10(self):
        base_health = 15
        base_force = 20
        health, force = calculate_mob_stats(base_health, base_force, 10)
        self.assertAlmostEqual(health, 21.75)
        self.assertAlmostEqual(force, 27.2)

    def test_creep_creation(self):
        creep = Creep(100, 100, 1)
        self.assertAlmostEqual(creep.health, 15)
        self.assertAlmostEqual(creep.damage, 20)

    def test_flyer_creation(self):
        flyer = Flyer(100, 100, 1)
        self.assertAlmostEqual(flyer.health, 15 / 1.10)
        self.assertAlmostEqual(flyer.damage, 20 * 1.2)

    def test_giant_creation(self):
        giant = Giant(100, 100, 1)
        self.assertAlmostEqual(giant.health, 15 * 1.4)
        self.assertAlmostEqual(giant.damage, 24 * 1.2)

if __name__ == '__main__':
    unittest.main()
