import pygame
player_sprite=pygame.transform.flip(pygame.image.load("Resources\\Sprites\\Remove_background_project_1.png"),1,0)
player_map_sprite=pygame.transform.scale(player_sprite,(100,100))
cubican_sprite=pygame.image.load("Resources\\Sprites\\cube.png")