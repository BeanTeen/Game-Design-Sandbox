import pygame
from Block import Block

class Target(Block):
    w=40
    h=40
    def __init__(self, x, y):
        super().__init__(x, y, Target.w, Target.h)
        self.hit=False
        self.h_timer=0
        self.hide=False

    def on_hit(self):
        self.hit=True
    
    def update(self, dt):
        if self.hit:
            self.h_timer+=dt
            if self.h_timer >=2.0:
                self.hide=True  
    
    def draw(self, screen):
        st_colors=['red', 'white', 'red', 'white', 'red']
        step_w=self.rect.width/len(st_colors)
        step_h=self.rect.height/len(st_colors)
        
        for i, color in enumerate(st_colors):
            if self.hit and color=='white':
                color='green'
            inner_rect = pygame.Rect(0, 0, int(self.rect.width-step_w*i), int(self.rect.height-step_h*i))
            inner_rect.center=self.rect.center
            pygame.draw.rect(screen, color, inner_rect)