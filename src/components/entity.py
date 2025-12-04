import pygame

RED = (255, 0, 0)

class Entity:
    def __init__(self, x, y, health, speed, image=None):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.speed = speed
        self.image = image
        
        if self.image:
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            # Create a default rect for placeholder drawing
            self.rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def update(self):
        # Update the rect position to match the x, y coordinates
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, RED, self.rect)  # Draw placeholder rect

        # Draw health bar
        if self.health < self.max_health:
            bar_width = self.rect.width
            bar_height = 5
            health_pct = self.health / self.max_health
            
            background_bar_rect = pygame.Rect(self.rect.left, self.rect.top - bar_height - 2, bar_width, bar_height)
            health_bar_rect = pygame.Rect(self.rect.left, self.rect.top - bar_height - 2, bar_width * health_pct, bar_height)
            
            pygame.draw.rect(screen, (255, 0, 0), background_bar_rect)
            pygame.draw.rect(screen, (0, 255, 0), health_bar_rect)
