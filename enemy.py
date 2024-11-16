from entity import *
from enemy import *
import random
import pygame

class EnemyController:
    def __init__(self, x, y, width, height, color):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        self.speed=10
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