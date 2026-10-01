import pygame
from Laser import Laser
from Character import Character

class Player(Character):
    def __init__(self, s_width, fl_y): # creates player with dimensions (w,h) and place them at (x,y)
        super().__init__(200, fl_y-100, 50, 50, 300, 'green', s_width)
        self.s_width = s_width
        self.jp=-750
        self.double_jumps=2
        self.lasers=[]
    
    def on_land(self):
        self.double_jumps=2
    
    def jump(self): # allows player to jump and double jump
        if self.double_jumps>0:
            self.vel_y=self.jp
            self.double_jumps-=1    
    
    def shoot(self):
        direction = 1 if self.facing_right else -1
        start_x = self.x + self.w if self.facing_right else self.x
        self.lasers.append(Laser(start_x, self.y + self.h // 2, direction))

    def handle_input(self): # allows player to move left and right, with shift key for faster movement
        keys=pygame.key.get_pressed() #reads key inputs (lets, nums, other)
        mods=pygame.key.get_mods() #reads mod key inputs (shift, ctrl)
        sprint_speed=120 if mods & pygame.KMOD_SHIFT else 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: #check if left or a key is pressed
            self.facing_right = False
            self.vel_x=-(self.speed+sprint_speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.facing_right=True
            self.vel_x = self.speed+sprint_speed
        else:
            self.vel_x=0
            
    def update(self, dt, platforms, floor_Y): #constantly runs to check inputs and status
        self.handle_input()
        super().update(dt, platforms, floor_Y)

        for laser in self.lasers:
            laser.update(dt)
        self.lasers = [l for l in self.lasers if 0 <= l.rect.x <= self.s_width]
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for laser in self.lasers:
            laser.draw(screen)