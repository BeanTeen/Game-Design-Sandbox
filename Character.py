import pygame
class Character:
    def __init__(self, x, y, w, h, speed, color, s_width):
        self.rect = pygame.Rect(x, y, w, h)
        self.x, self.y = float(x), float(y)
        self.w, self.h = w, h
        self.speed=speed
        self.color=color
        self.s_width = s_width
        self.vel_x=0
        self.vel_y=0
        self.gravity=2500
        self.facing_right=True
    
    def update(self, dt, platforms, floor_Y):
        #Horizontal movement
        self.x +=self.vel_x * dt
        self.rect.x=int(self.x)
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom > platform.rect.top +10:
                    continue
                if self.vel_x>0:
                    self.rect.right=platform.rect.left
                elif self.vel_x<0:
                    self.rect.left=platform.rect.right
                self.x=float(self.rect.x)
        
        #Veritcal movement
        prev_y=self.y
        self.vel_y+=self.gravity * dt
        self.y += self.vel_y * dt
        self.rect.y = int(self.y)
        
        if self.rect.bottom >= floor_Y:
            self.rect.bottom=floor_Y
            self.vel_y=0
            self.y=float(self.rect.y)
            self.on_land()
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y>0 and prev_y +self.h <=platform.rect.top+20:
                    self.rect.bottom=platform.rect.top
                    self.vel_y=0
                    self.y=float(self.rect.y)
                    self.on_land()
        
        if self.rect.left > self.s_width:
            self.rect.right=0
            self.x=float(self.rect.x)
        elif self.rect.right < 0:
            self.rect.left=self.s_width
            self.x=float(self.rect.x)

    def on_land(self):
        pass