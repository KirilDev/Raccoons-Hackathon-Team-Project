from random import * #Idk why i'm importing this here
from math import *
import pygame
import json
pygame.init()
class Map:
    def __init__(self):
        self.heightmap=[
            [1,1,1],
            [1,0,1],
            [1,1,1],
            ]
    def load_from_path(self,path,scale_to=1):
        self.path=path
        loaded_image=pygame.image.load(path+".png")
        with open(path+".json") as loaded_data:
            map_data=json.loads(loaded_data.read())
        new_heightmap=[]
        #new_map_layout_tiles_lesser=[]
        for y in range(loaded_image.get_height()):
            heightmap_tile_line=[]
            for x in range(loaded_image.get_width()):
                loaded_pixel=str(loaded_image.get_at((x,y))[:-1])
                if loaded_pixel in map_data["Layout Data"]:
                    heightmap_tile_line.append(map_data["Layout Data"][loaded_pixel]["Height"])
                else:
                    heightmap_tile_line.append(1)
            new_heightmap.append(heightmap_tile_line)
        self.discovered_surfacee=pygame.Surface((loaded_image.get_width()*100, 1))
        self.heightmap=new_heightmap
        self.base_image=pygame.transform.scale_by(loaded_image,scale_to)
#test_map=Map()
#test_map.load_from_path("Resources/Maps/Test_Map/alpha")