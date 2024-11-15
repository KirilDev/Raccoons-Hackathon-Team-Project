from math import *
from random import *
import pygame
import os
import json
matheon_data={}
for root,dirs,files in os.walk(r"Resources\\Matheon Data\\"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root,file),"r") as read_file:
                matheon_data[file[:-5]]=json.loads(read_file.read())
class Battle_Matheon:
    def __init__(self,type,level):
        self.type=type
        self.level=level
        self.data=matheon_data[self.type]
        self.level_exponent=1+self.level/7
        self.max_health=(1+self.data["Attributes"]["Health"])**self.level_exponent*30
        self.defense=(1+self.data["Attributes"]["Defense"])**self.level_exponent
        self.attack=(1+self.data["Attributes"]["Attack"])**self.level_exponent
        self.speed=(1+self.data["Attributes"]["Speed"])**self.level_exponent
    
    def use_move(self,move_name):
        pass
#This is used for Matheon Testing
new_matheon=Battle_Matheon("Cubican",1)