import pygame

class Block:
    def __init__(self, x, y, w, h): # creates platf orms at coords (x,y) with dimensions (h,w)
        self.rect = pygame.Rect(x, y, w, h)
        
    def draw(self, screen):
        # Draws the block on the provided surface using its assigned color
        pygame.draw.rect(screen, self.color, self.rect)