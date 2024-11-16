from random import *
import pygame
from math import *
from player import *
from map import *
from matheon import *

from time import time
import enemy
pygame.init()
screen=pygame.display.set_mode((0,0))
screen_size=screen.get_size()
win=pygame.Surface((2000,1000))
pygame.display.set_caption('The Raccoons Hackathon Project - Placehoolder')
minimal_size = (200, 150)
minimal_surface = pygame.Surface(minimal_size)
scaled_map = pygame.transform.scale(win, minimal_size)

def mainloop(win,screen,data={}):
    run=True
    test_map=Map()
    test_map.load_from_path("Resources/Maps/Test_Map/alpha",100)
    test_map.base_image=pygame.image.load("Resources/maps/Test_Map/The Interface.png")
    player=Player()
    
    player.entity.x=1
    player.entity.y=4
    player.entity.z=1
    player.display_x=player.entity.x
    player.display_z=player.entity.z
    
    enemy=EnemyController(1, 1, 50, 60, (255, 0, 0))
    
    enemy.entity.x=1
    enemy.entity.y=4
    enemy.entity.z=1
    enemy.x=enemy.entity.x
    enemy.z=enemy.entity.z
    
    map_visibility_surface=pygame.Surface((len(test_map.heightmap[0])*100,len(test_map.heightmap)*100))    
    map_semivisible_surface=pygame.Surface((len(test_map.heightmap[0]),len(test_map.heightmap)))
    map_semivisible_surface.set_colorkey((255,255,255))
    map_visibility_surface.set_colorkey((255,255,255))
    map_visibility_surface.set_alpha(100)
    player.entity.update_vision(test_map.heightmap)
    
    def update_map():
        map_visibility_surface.fill((0,0,0))
        for i in player.entity.squares_seen:
            pygame.draw.rect(map_visibility_surface,(255,255,255),(i[0]*100,i[2]*100,100,100))
            pygame.draw.rect(test_map.discovered_surface,(255,255,255),(i[0]*100,i[2]*100,100,100))
        for i in player.entity.walls_seen:
            pygame.draw.rect(map_visibility_surface,(255,255,255),(i[0]*100,i[2]*100,100,100))
            pygame.draw.rect(test_map.discovered_surface,(255,255,255),(i[0]*100,i[2]*100,100,100))
            
    update_map()
    camera_x=0
    camera_y=0
    frame=0
    clock=pygame.time.Clock()
    while run: #Mainloop
        pygame.display.flip()
        print(player.display_x, player.display_z)
        frame+=1
        clock.tick(144)
        #print(clock.get_fps())
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[27]: run=False
        if frame%10==0:
            player_moved=False
            if keys[pygame.K_UP]:
                player.move(test_map,"Up")
                player_moved=True
            if keys[pygame.K_DOWN]:
                player.move(test_map,"Down")
                player_moved=True
            if keys[pygame.K_RIGHT]:
                player.move(test_map,"Right")
                player_moved=True
            if keys[pygame.K_LEFT]:
                player.move(test_map,"Left")
                player_moved=True
            if player_moved:
                #print(player.entity.x)
                update_map()
        player.update_state()   
        camera_x=player.display_x*100-950
        camera_y=player.display_z*100-450
        
        win.fill((0,0,0))
        enemy.enemyMove()
        enemy.draw(win)
        win.blit(test_map.base_image,(-camera_x,-camera_y))
        
        #for x in range(21):
            #true_x=player.entity.x-9
            #pygame.draw.line(win,(255,255,255),(x*100-camera_x%100,0),(x*100-camera_x%100,1000),3)
            #for y in range(11):
                #true_x=player.entity.y-4
                #pygame.draw.line(win,(255,255,255),(0,y*100-camera_y%100),(2000,y*100-camera_y%100),3)
                #pass
        #pygame.draw.rect(win,(255,0,255),(950,450,100,100))
        win.blit(player_map_sprite,(960,460))
        # win.blit(test_map.discovered_surface,(-camera_x,-camera_y))
        # win.blit(map_visibility_surface,(-camera_x,-camera_y))
        screen.blit(pygame.transform.scale(win,screen_size),(0,0))
        pygame.display.update()
    # def draw_minimap():
    #     minimap_surface.blit(scaled_map, (0,0))

    #     player_x, player_y = player.rect.center

    #     minimap_x = int(player_x * minimal_size[0] / win.get_width())
    #     minimap_y = int(player_y * minimal_size[0] / win.get_width())

    #     pygame.draw.rect(minimal_surface, (255,0,0), (minimap_x - 2, minimap_y - 2,4,4))
    #     win.blit(minimal_surface, (10,10))
# Battle(new_matheon1,new_matheon2,screen=screen,win=win)
mainloop(win,screen)
pygame.quit()