from entity import *
from enemy import *
import random
import pygame

# pygame.init()
# screen = pygame.display.set_mode((2000, 1000))
#unseen_surface=pygame.Surface((128,128))
#unseen_surface.set_alpha()
class Player:
    def __init__(self):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        self.entity.health_level=100
        self.player_rect = pygame.Rect(0,0,0,0)
        #self.discovered_surface(())
    def move(self,heightmap,direction):
        if direction=="Down":
            if self.entity.z<len(heightmap.heightmap)-1:
                if heightmap.heightmap[self.entity.z+1][self.entity.x]<=self.entity.y:
                    self.entity.z+=1
        if direction=="Up":
            if self.entity.z>0:
                if heightmap.heightmap[self.entity.z-1][self.entity.x]<=self.entity.y:
                    self.entity.z-=1
        if direction=="Right":
            if self.entity.x<len(heightmap.heightmap[0])-1:
                if heightmap.heightmap[self.entity.z][self.entity.x+1]<=self.entity.y:
                    self.entity.x+=1
        if direction=="Left":
            if self.entity.x>0:
                if heightmap.heightmap[self.entity.z][self.entity.x-1]<=self.entity.y:
                    self.entity.x-=1
        self.entity.update_vision(heightmap.heightmap)

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
#     # enemy.draw(screen)

#     # Entity.x += Entity.entity.x
#     # Entity.z += Entity.entity.z
#     # # Entity.player_rect.x = Entity.entity.x
#     # # Entity.player_rect.z = Entity.entity.z
    
#     # # if player_rect.colliderect(pygame.Rect(enemy.x, enemy.y, 20, 20)):
#     # #     player_health -= enemy.damage
