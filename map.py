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

        self.door_data={}
        self.doors=[]

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
                    if "Data" in map_data["Layout Data"][loaded_pixel]:
                        if "Door" in map_data["Layout Data"][loaded_pixel]["Data"]:
                            self.doors.append((x,map_data["Layout Data"][loaded_pixel]["Height"],y))
                else:
                    print("Unknown Pixel:",loaded_pixel)
                    heightmap_tile_line.append(1)
            new_heightmap.append(heightmap_tile_line)
        if "Door Data" in map_data:
            for i in map_data["Door Data"]:
                start_and_end=i.split("-")
                for ii in range(int(start_and_end[0]),int(start_and_end[1])+1):
                    self.door_data[self.doors[ii]]={
                        "Destination Path":map_data["Door Data"][i]["Destination Map Path"]
                    }
        self.discovered_surface=pygame.Surface((loaded_image.get_width()*scale_to,loaded_image.get_height()*scale_to))
        #self.discovered_surface.set_alpha(120)
        self.discovered_surface.set_colorkey((255,255,255))
        self.heightmap=new_heightmap
        #for i in self.heightmap:
        #    print(i)
        if "Starting Position" in map_data:
            self.starting_position=map_data["Starting Position"]
        else:
            self.starting_position={
                "X":1,
                "Y":0,
                "Z":1
            }
        if not "Overlay Image" in map_data:
            self.base_image=pygame.transform.scale_by(loaded_image,scale_to)
        else:
            self.base_image=pygame.transform.scale(pygame.image.load(map_data["Overlay Image"]),(loaded_image.get_width()*scale_to,loaded_image.get_height()*scale_to))
#test_map=Map()
#test_map.load_from_path("Resources/Maps/Test_Map/alpha")