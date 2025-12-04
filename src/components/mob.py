import pygame
from .entity import Entity

import pygame
from .entity import Entity
import math

class Mob(Entity):
    def __init__(self, x, y, health, speed, damage, mob_type, target=None, image=None):
        super().__init__(x, y, health, speed, image)
        self.damage = damage
        self.mob_type = mob_type
        self.target = target
        self.pos = pygame.math.Vector2(x, y)
        self.attack_cooldown = 1  # seconds
        self.last_attack_time = 0


        self.gold_reward = 0
        self.exp_reward = 0
        self.flesh_reward = 0

        if self.mob_type == 'rempant':
            self.gold_reward = 1
            self.exp_reward = 1
            self.flesh_reward = 1
        elif self.mob_type == 'volant':
            self.gold_reward = 2
            self.exp_reward = 2
        elif self.mob_type == 'geant':
            self.gold_reward = 5
            self.exp_reward = 5
            self.flesh_reward = 3

    def find_target(self, troops, furnace):
        closest_target = None
        min_dist = float('inf')

        # Consider all troops as potential targets
        for troop in troops:
            if troop.is_alive():
                dist = math.hypot(self.x - troop.x, self.y - troop.y)
                if dist < min_dist:
                    min_dist = dist
                    closest_target = troop

        # Consider the furnace as a potential target
        if furnace.is_alive():
            dist_to_furnace = math.hypot(self.x - furnace.x, self.y - furnace.y)
            if dist_to_furnace < min_dist:
                min_dist = dist_to_furnace
                closest_target = furnace

        self.target = closest_target

    def attack(self):
        if self.target and self.target.is_alive():
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            if dist < 50: # Attack range
                current_time = pygame.time.get_ticks() / 1000
                if current_time - self.last_attack_time > self.attack_cooldown:
                    self.target.take_damage(self.damage)
                    self.last_attack_time = current_time

    def update(self, troops, furnace, mobs):
        self.find_target(troops, furnace)
        self.attack()
        
        movement_vector = pygame.math.Vector2(0, 0)

        # Movement towards target
        if self.target:
            direction = pygame.math.Vector2(self.target.rect.centerx, self.target.rect.centery) - self.pos
            if direction.length() > 1:
                direction.normalize_ip()
                movement_vector += direction

        # Separation from other mobs
        separation_vector = pygame.math.Vector2(0, 0)
        for mob in mobs:
            if mob is not self:
                dist = self.pos.distance_to(mob.pos)
                if dist < 30: # Separation radius
                    if dist > 0:
                        flee_vector = self.pos - mob.pos
                        flee_vector.normalize_ip()
                        separation_vector += flee_vector
        
        if separation_vector.length() > 0:
            separation_vector.normalize_ip()
        
        # Combine movement and separation vectors
        # Give more weight to separation to avoid overlap
        total_movement = movement_vector * 0.5 + separation_vector * 1.0 

        if total_movement.length() > 0:
            total_movement.normalize_ip()
            self.pos += total_movement * self.speed
            self.x = self.pos.x
            self.y = self.pos.y
        
        super().update()
