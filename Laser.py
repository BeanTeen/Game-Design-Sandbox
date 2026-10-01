import pygame

class Laser:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 15, 5)
        self.pos_x = float(x)
        self.speed = 900 * direction
        self.color = 'red'

    def update(self, dt):
        self.pos_x += self.speed * dt
        self.rect.x = int(self.pos_x)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)