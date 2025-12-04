import pygame
from .entity import Entity
from .mob import Mob
import math

class Troop(Entity):
    def __init__(self, x, y, health, speed, damage, troop_type, attack_range, attack_cooldown, image=None):
        super().__init__(x, y, health, speed, image)
        self.damage = damage
        self.troop_type = troop_type
        self.stamina = 100
        self.target = None
        self.pain_consumption_rate = 0.1
        self.has_pain = True
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0

    def find_target(self, mobs):
        if self.target and self.target.is_alive() and math.hypot(self.x - self.target.x, self.y - self.target.y) < self.attack_range:
            return  # Keep current target if it's still valid

        potential_targets = []
        for mob in mobs:
            if mob.is_alive():
                if self.troop_type == 'archer':
                    potential_targets.append(mob)
                elif mob.mob_type != 'volant':
                    potential_targets.append(mob)

        best_target = None
        if self.troop_type == 'assassin':
            min_x = float('inf')
            for mob in potential_targets:
                dist = math.hypot(self.x - mob.x, self.y - mob.y)
                if dist < self.attack_range:
                    if mob.x < min_x:
                        min_x = mob.x
                        best_target = mob
        else:
            min_dist = float('inf')
            for mob in potential_targets:
                dist = math.hypot(self.x - mob.x, self.y - mob.y)
                if dist < min_dist:
                    min_dist = dist
                    best_target = mob
        
        self.target = best_target

    def attack(self):
        if self.target and self.target.is_alive():
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            if dist < self.attack_range:
                current_time = pygame.time.get_ticks() / 1000
                if current_time - self.last_attack_time > self.attack_cooldown:
                    damage = self.damage
                    if not self.has_pain:
                        damage /= 2
                    self.target.take_damage(damage)
                    self.last_attack_time = current_time
            else:
                self.target = None
        else:
            self.target = None

    def update(self, mobs):
        self.find_target(mobs)

        if self.speed > 0 and self.target:
            direction = pygame.math.Vector2(self.target.rect.centerx, self.target.rect.centery) - (self.x, self.y)
            # Move until in 80% of attack range
            if direction.length() > self.attack_range * 0.8:
                direction.normalize_ip()
                pos = pygame.math.Vector2(self.x, self.y)
                pos += direction * self.speed
                self.x = pos.x
                self.y = pos.y

        self.attack()
        super().update()
