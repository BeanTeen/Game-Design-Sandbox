import ctypes
import pygame
import configparser
import threading
import time
from Text import Text
from Player import Player
from Target import Target
from Network import Network
from Platform import Platform
import Server
ctypes.windll.user32.SetProcessDPIAware() #fixes fuckass windows scaling bullshit
class GameProt:
    def __init__(self): #*1
        pygame.init() 
        pygame.font.init()
        self.width,self.height=1920, 1080
        self.size=(self.width, self.height) # Window dimensions
        self.floor_Y = self.height - 100 #set floor height
        self.state='menu' #start at menu
        self.timer=0 # Global timer for animations
        self.colors=['red','green','blue','yellow', 'purple', 'orange']
        self.color_index=1
        self.fps=60
        self._load_settings() # Initialize settings from file
        self.bcolor='ivory'
        self.fcolor='grey'

        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption("Game")
        self.running=True
        
        self.net=None
        self.p_data=None
        self.net_dummies={}
        
        self.player=Player(self.width, self.floor_Y)
        self.player.color = self.colors[self.color_index]
        # Floor and some floating platforms
        self.platforms = [
            Platform(750, self.floor_Y-100, 200, 20), 
            Platform(1200, self.floor_Y-200, 200, 20),
            Platform(250, self.floor_Y-350, 200, 20)]#list of platforms for collision detection
        
        self.targets=[] # List to store target objects
        for p in self.platforms:
            # Position targets above platforms
            t_x=p.rect.centerx-(Target.w//2)
            t_y=(p.rect.top-Target.h)-20
            self.targets.append(Target(t_x,t_y))
        
        self.reg_font=self.fonter(30) # Font for standard text
        self.title_font=self.fonter(60)
        self.small_font=self.fonter(20)
        self.m_title=Text("Press SPACE to Start", self.title_font, self.width//2, self.height//2)
        self.m_sp = Text("1: Singleplayer", self.reg_font, self.width//2, self.height//2 - 40)
        self.m_host = Text("2: Host Multiplayer", self.reg_font, self.width//2, self.height//2 + 10)
        self.m_join = Text("3: Join (Localhost/LAN)", self.reg_font, self.width//2, self.height//2 + 60)
        self.m_settings=Text("S: Settings", self.reg_font, self.width//2, self.height//2 + 50)
        self.m_quit=Text("ESC: Quit", self.small_font, self.width//2, self.height- 100)
        
        self.set_fps = Text(f"Target FPS: {self.fps} (UP/DOWN)", self.reg_font, self.width//2, self.height//2 - 60)
        self.set_col = Text(f"Player Color: {self.colors[self.color_index]} (LEFT/RIGHT)", self.reg_font, self.width//2, self.height//2 - 20)
        self.set_quit = Text("ESC/SPACE: Exit Settings", self.reg_font, self.width//2, self.height//2 + 60)
        self.set_save = Text("ENTER: Save Settings", self.reg_font, self.width//2, self.height//2 + 100)
        self.game_quit = Text("ESC: QUIT", self.small_font, 20, self.height-50, center=False)
    
    def game_mode(self, mode, host_ip="127.0.0.1"):
        if mode in ("singleplayer", "host"):
            bind_ip="0.0.0.0" if mode == "host" else "127.0.0.1"
            server_thread = threading.Thread(target=Server.start_server, args=(bind_ip, 5555), daemon=True)
            server_thread.start()
            time.sleep(0.1)
            self.net = Network("127.0.0.1", 5555)
        elif mode == "join":
            self.net = Network(host_ip, 5555)

        self.p_data = self.net.get_player() if self.net else None
        if self.p_data:
            self.player.x = float(self.p_data["x"])
            self.player.y = float(self.p_data["y"])
            self.player.rect.x = self.p_data["x"]
            self.player.rect.y = self.p_data["y"]
            self.state = "game"
        else:
            print("Failed to connect")

    def _load_settings(self):
        # Read settings from settings.ini file
        config=configparser.ConfigParser() #*2
        config.read('settings.ini')
        if 'Settings' in config:
            try:
                self.fps=config.getint('Settings', 'fps', fallback=60) 
                self.color_index=config.getint('Settings', 'color_index', fallback=1)
            except ValueError:
                pass
            
    def _save_settings(self):
        # Write current settings to settings.ini file
        config=configparser.ConfigParser()
        config['Settings'] = {'fps': str(self.fps), 'color_index': str(self.color_index)}
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
            
    def fonter(self, size, style='courier'):
        # Helper to create system fonts
        return pygame.font.SysFont(style, size)
    
    def update(self, dt): #*3
        self.timer+=dt
        for event in pygame.event.get(): # Event loop
            et=event.type
            ek=getattr(event, 'key', None)
            if et==pygame.QUIT:
                self.running=False

            if self.state=='menu':
                if et==pygame.KEYDOWN:
                    if ek==pygame.K_1:
                        self.game_mode("singleplayer")
                    elif ek==pygame.K_2:
                        self.game_mode("host")
                    elif ek == pygame.K_3:
                        self.game_mode("join", "127.0.0.1")
                    elif ek==pygame.K_s:
                        self.state='settings'
                    elif ek==pygame.K_ESCAPE:
                        self.running=False
            elif self.state=='settings':
                if et==pygame.KEYDOWN:
                    if ek==pygame.K_UP:
                        self.fps = min(self.fps+5, 120)
                        self.set_fps.update(f"Target FPS: {self.fps} (UP/DOWN)")
                    elif ek==pygame.K_DOWN:
                        self.fps = max(self.fps-5, 10)
                        self.set_fps.update(f"Target FPS: {self.fps} (UP/DOWN)")
                    elif ek==pygame.K_RIGHT:
                        self.color_index= (self.color_index+1) % len(self.colors)
                        self.player.color=self.colors[self.color_index]
                        self.set_col.update(f"Player Color: {self.colors[self.color_index]} (LEFT/RIGHT)")
                    elif ek==pygame.K_LEFT:
                        self.color_index=(self.color_index-1) % len(self.colors)
                        self.player.color=self.colors[self.color_index]
                        self.set_col.update(f"Player Color: {self.colors[self.color_index]} (LEFT/RIGHT)")
                    elif ek==pygame.K_RETURN:
                        self._save_settings()
                    elif ek==pygame.K_ESCAPE or ek==pygame.K_SPACE:
                        self.state='menu'
            elif self.state=='game':
                if et==pygame.KEYDOWN:
                    if ek==pygame.K_UP or ek==pygame.K_w:
                        self.player.jump()
                    if ek==pygame.K_SPACE:
                        self.player.shoot()
                    if ek==pygame.K_ESCAPE:
                        self.state='menu'
        if self.state=='game':        
            self.player.update(dt, self.platforms, self.floor_Y) # Update player physics

            if self.net:
                localState = {
                    "x": self.player.rect.x,
                    "y": self.player.rect.y,
                    "color": self.player.color,
                    "facing_right": self.player.facing_right
                }
                connected_players=self.net.send(localState)

                if connected_players:
                    active_ids=set()
                    for p_id, p_data in connected_players.items():
                        if p_data["x"]==self.player.rect.x and p_data["y"] == self.player.rect.y:
                            continue
                        active_ids.add(p_id)
                        if p_id not in self.net_dummies:
                            self.net_dummies[p_id]=Player(self.width, self.floor_Y)
                        
                        self.net_dummies[p_id].rect.x = p_data["x"]
                        self.net_dummies[p_id].rect.y = p_data["y"]
                        self.net_dummies[p_id].x = float(p_data["x"])
                        self.net_dummies[p_id].y = float(p_data["y"])
                        self.net_dummies[p_id].color = p_data["color"]
                        self.net_dummies[p_id].facing_right = p_data.get("facing_right", True)
                    self.net_dummies={k: v for k, v in self.net_dummies.items() if k in active_ids}

            for target in self.targets:
                target.update(dt)
            self.targets = [t for t in self.targets if not t.hide] # Remove hidden targets
            
            for laser in self.player.lasers[:]:
                for target in self.targets: # Check laser-target collisions
                    if not target.hit and laser.rect.colliderect(target.rect):
                        target.on_hit()
                        if laser in self.player.lasers:
                            self.player.lasers.remove(laser)
                        break
        
    def draw(self):
        self.screen.fill(self.bcolor) # Clear screen
        
        if self.state=='menu':
            self.m_sp.draw(self.screen)
            self.m_host.draw(self.screen)
            self.m_join.draw(self.screen)
            self.m_settings.draw(self.screen)
            self.m_quit.draw(self.screen)
            
        elif self.state=='settings':
            self.set_fps.draw(self.screen)
            self.set_col.draw(self.screen)
            
            # Draw a preview box of the player color
            box_x=self.set_col.rect.right + 10
            box_y=self.set_col.rect.centery - 15
            pygame.draw.rect(self.screen, self.colors[self.color_index], (box_x, box_y, 30, 30))

            # Draw settings navigation instructions
            self.set_quit.draw(self.screen)
            self.set_save.draw(self.screen)
        elif self.state=='game':
            # Draw the ground/floor
            pygame.draw.rect(self.screen, self.fcolor, (0, self.floor_Y, self.width, self.height-self.floor_Y))
            # Render all active platforms
            for platform in self.platforms:
                platform.draw(self.screen)
            for target in self.targets:
                target.draw(self.screen)
            #draw other players if they exist
            for dummy in self.net_dummies.values():
                dummy.draw(self.screen)
            
            self.player.draw(self.screen)
            self.game_quit.draw(self.screen)

        pygame.display.flip() # Update display
        
    def run(self):
        clock=pygame.time.Clock()
        while self.running:
            dt = clock.tick(self.fps)/1000 # Delta time in seconds
            self.update(dt)
            self.draw()
            
if __name__=="__main__":
    game=GameProt()
    game.run()