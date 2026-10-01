import pygame

class Text:
    def __init__(self, text, font, x, y, color='black', center=True):
        self.text=text
        self.font=font
        self.color=color
        self.x=x
        self.y=y
        self.center=center
        self.update(text)
        
    def update(self, text):
        self.text=str(text)
        self.surface=self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center=(self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)