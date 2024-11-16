from entity import *
from enemy import *
import random
import pygame

class EnemyController:
    def __init__(self, x, y, width, height, color):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        self.speed=1
        self.entity.health_level=100
        self.x=self.entity.x
        self.z=self.entity.z
        self.state={}
        self.heightmap=None
        self.direction = 'right'
        self.width=width
        self.height=height
        self.color=color
        
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def enemyMove(self):
        if self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'up':
            self.z -= self.speed
        elif self.direction == 'down':
            self.z += self.speed

        if random.randint(0, 100) < 10:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    # def update_state(self):
    #     if self.state!={}:
    #         if self.state["Type"]=="Moving Animation":
    #             self.state["Frames Left"]-=1
    #             if self.state["Direction"]=="Up":
    #                 self.display_z=self.entity.z-1+0.1*self.state["Frames Left"]
    #             if self.state["Direction"]=="Down":
    #                 self.display_z=self.entity.z+1-0.1*self.state["Frames Left"]
    #             if self.state["Direction"]=="Left":
    #                 self.display_x=self.entity.x-1+0.1*self.state["Frames Left"]
    #             if self.state["Direction"]=="Right":
    #                 self.display_x=self.entity.x+1-0.1*self.state["Frames Left"]
                
    #             if self.state["Frames Left"]==0:
    #                 if self.state["Direction"]=="Up":
    #                     self.entity.z-=1
    #                 if self.state["Direction"]=="Down":
    #                     self.entity.z+=1
    #                 if self.state["Direction"]=="Left":
    #                     self.entity.x-=1
    #                 if self.state["Direction"]=="Right":
    #                     self.entity.x+=1
    #                 if self.heightmap!=None:
    #                     self.entity.update_vision(self.heightmap)
    #                 self.display_x=self.entity.x
    #                 self.display_z=self.entity.z
    #                 self.state={}
    # # Entity.x += Entity.entity.x
    # Entity.z += Entity.entity.z
    # Entity.player_rect.x = Entity.entity.x
    # Entity.player_rect.z = Entity.entity.z
    
    # if player_rect.colliderect(pygame.Rect(enemy.x, enemy.y, 20, 20)):
    #     player_health -= enemy.damage
    # , x, z, speed