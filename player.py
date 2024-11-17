from entity import *
from enemy import *
import random
import pygame

class Player:
    def __init__(self):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        self.display_x=self.entity.x
        self.display_z=self.entity.z
        self.state={}
        self.heightmap=None
        self.entity.health_level=100
        self.player_rect = pygame.Rect(0,0,0,0)
        self.standing_on=[]
        #self.discovered_surface(())
    def move(self,heightmap,direction):
        if self.state=={}:
            if direction=="Down":
                if self.entity.z<len(heightmap.heightmap)-1:
                    if heightmap.heightmap[self.entity.z+1][self.entity.x]<=self.entity.y:
                        #self.entity.z+=1
                        self.state={
                            "Type":"Moving Animation",
                            "Direction":"Down",
                            "Frames Left":10
                        }
            if direction=="Up":
                if self.entity.z>0:
                    if heightmap.heightmap[self.entity.z-1][self.entity.x]<=self.entity.y:
                        #self.entity.z-=1
                        self.state={
                            "Type":"Moving Animation",
                            "Direction":"Up",
                            "Frames Left":10
                        }
            if direction=="Right":
                if self.entity.x<len(heightmap.heightmap[0])-1:
                    if heightmap.heightmap[self.entity.z][self.entity.x+1]<=self.entity.y:
                        #self.entity.x+=1
                        self.state={
                            "Type":"Moving Animation",
                            "Direction":"Right",
                            "Frames Left":10
                        }
            if direction=="Left":
                if self.entity.x>0:
                    if heightmap.heightmap[self.entity.z][self.entity.x-1]<=self.entity.y:
                        #self.entity.x-=1
                        self.state={
                            "Type":"Moving Animation",
                            "Direction":"Left",
                            "Frames Left":10
                        }
            if direction=="Don't move, this is for setup":
                self.state={
                    "Type":"Moving Animation",
                    "Direction":"Neither And All",
                    "Frames Left":1
                } #Needed to setup the code
        if self.heightmap==None:
            self.heightmap=heightmap.heightmap
            self.map=heightmap
    def update_state(self):
        if self.state!={}:
            if self.state["Type"]=="Moving Animation":
                self.state["Frames Left"]=max(0,self.state["Frames Left"]-10)
                if self.state["Direction"]=="Up":
                    self.display_z=self.entity.z-1+0.1*self.state["Frames Left"]
                if self.state["Direction"]=="Down":
                    self.display_z=self.entity.z+1-0.1*self.state["Frames Left"]
                if self.state["Direction"]=="Left":
                    self.display_x=self.entity.x-1+0.1*self.state["Frames Left"]
                if self.state["Direction"]=="Right":
                    self.display_x=self.entity.x+1-0.1*self.state["Frames Left"]
                
                if self.state["Frames Left"]==0:
                    if self.state["Direction"]=="Up":
                        self.entity.z-=1
                    if self.state["Direction"]=="Down":
                        self.entity.z+=1
                    if self.state["Direction"]=="Left":
                        self.entity.x-=1
                    if self.state["Direction"]=="Right":
                        self.entity.x+=1
                    if self.heightmap!=None:
                        self.entity.update_vision(self.heightmap)
                    self.standing_on=[]
                    if "Door" in self.map.special_data:
                        for i in self.map.special_data["Door"]:
                            if self.entity.x==i[0] and self.entity.y==i[1] and self.entity.z==i[2]:
                                self.standing_on.append({
                                    "Type":"Door",
                                    "Redirects To":self.map.special_data["Door"][i]["Door Destination Path"]
                                })
                    if "Exit Level" in self.map.special_data:
                        for i in self.map.special_data["Exit Level"]:
                            if self.entity.x==i[0] and self.entity.y==i[1] and self.entity.z==i[2]:
                                self.standing_on.append({
                                    "Type":"Exit"
                                })
                    self.display_x=self.entity.x
                    self.display_z=self.entity.z
                    self.state={}
            
# class EnemyController:
#     def __init__(self, x, z, speed, player_health):
#         self.x = x
#         self.z = z
#         self.speed = speed
#         self.direction = 'right'
#         self.player_health = 0

#     def enemyMove(self):
#         if self.direction == 'right':
#             self.x += self.speed
#         elif self.direction == 'left':
#             self.x -= self.speed
#         elif self.direction == 'up':
#             self.z -= self.speed
#         elif self.direction == 'down':
#             self.z += self.speed

#         if random.randint(0, 100) < 10:
#             self.direction = random.choice(['up', 'down', 'left', 'right'])
    
#     def draw(self, screen):
#         pygame.draw.rect(screen, (255, 0, 0), (self.x, self.z, 20, 20))

# enemy = EnemyController(100, 100, 1, 100)

# while True:
#     enemy.enemyMove()

#     Entity.x += Entity.entity.x
#     Entity.z += Entity.entity.z
#     Entity.player_rect.x = Entity.entity.x
#     Entity.player_rect.z = Entity.entity.z
    
#     if player_rect.colliderect(pygame.Rect(enemy.x, enemy.y, 20, 20)):
#         player_health -= enemy.damage