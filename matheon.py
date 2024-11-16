from math import *
from random import *
import pygame
import os
import json
matheon_data={}
for root,dirs,files in os.walk(r"Resources/Matheon Data/"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root,file),"r") as read_file:
                matheon_data[file[:-5]]=json.loads(read_file.read())

move_data={}
for root,dirs,files in os.walk(r"Resources/Matheon Moves/"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root,file),"r") as read_file:
                move_data[file[:-5]]=json.loads(read_file.read())
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
        self.known_moves=[]
        for i in self.data["Starting Moves"]:
            if i["Type"]=="Pool":
                self.known_moves+=sample(i["Possible Elements"],i["Selected Elements"])
        print(self.known_moves)
        self.enemy=None
    def use_move(self,move_name):
        self.used_move=move_data[move_name]
        for action in self.used_move["Actions"]:

            self.do_action(action)
    def do_action(self,action):
        print(action)
        if "If" in action:
            if action["If"]["Type"]=="Random":
                if random()<action["If"]["Chance"]:
                    for nested_action in action["If"]["Then"]:
                        self.do_action(nested_action)
        if "Deal Damage" in action:
            self.enemy.deal_damage(self,action["Deal Damage"])
    def deal_damage(self,attacker,how_much):
        self.taken_damage=attacker.attack*how_much*(2/3+random())/self.defense
        print(self.taken_damage)
def link(p1,p2):
    p1.enemy=p2
    p2.enemy=p1
#This is used for Matheon Testing
new_matheon1=Battle_Matheon("Cubican",1)
new_matheon2=Battle_Matheon("Cubican",1)
link(new_matheon1,new_matheon2)
new_matheon1.use_move("Brute Force")
#print(new_matheon2.taken_damage)