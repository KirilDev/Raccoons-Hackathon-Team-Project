from math import *
from random import *
from sprite_def import *
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
for root,dirs,files in os.walk(r"Resources\\Matheon Moves\\"):
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
        self.base_max_health=(1+self.data["Attributes"]["Health"])**self.level_exponent*30
        self.base_defense=(1+self.data["Attributes"]["Defense"])**self.level_exponent
        self.base_attack=(1+self.data["Attributes"]["Attack"])**self.level_exponent
        self.base_speed=(1+self.data["Attributes"]["Speed"])**self.level_exponent
        self.known_moves=[]
        for i in self.data["Starting Moves"]:
            if i["Type"]=="Pool":
                self.known_moves+=sample(i["Possible Elements"],i["Selected Elements"])
        self.enemy=None
        self.new_deffense=self.base_defense
        self.new_attack=self.base_attack
        self.new_max_health=self.base_max_health
        self.new_speed=self.base_speed
        self.sprite=pygame.transform.scale(pygame.image.load(self.data["Sprite Path"]),(400,400))
    def use_move(self,move_name):
        self.used_move=move_data[move_name]
        for action in self.used_move["Actions"]:
            self.do_action(action)
    def do_action(self,action):
        #print(action)
        if "If" in action:
            if action["If"]["Type"]=="Random":
                if random()<action["If"]["Chance"]:
                    for nested_action in action["If"]["Then"]:
                        self.do_action(nested_action)
        if "Deal Damage" in action:
            self.enemy.deal_damage(self,action["Deal Damage"])
    def deal_damage(self,attacker,how_much):
        self.taken_damage=attacker.attack*how_much*(2/3+random())/self.defense
        self.health-=self.taken_damage
        print(self.taken_damage)
    def apply_effect(self,effect,by_who=None):
        if "Frail" in effect:
            self.defense*=1-effect["Frail"]
def Battle(controlled_by_player,attacked_player,win,screen):
    defender=controlled_by_player
    attacker=attacked_player
    run=True
    frame=0
    is_battle_screen_running=True
    clock=pygame.time.Clock()
    dark_screen=pygame.Surface((2000,1000))
    animation_data={
        "Type":"Transition Start",
        "Frames Left":72
        }
    while run and is_battle_screen_running: #Mainloop
        frame+=1
        clock.tick(144)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[27]: run=False
        win.fill((25,25,25))
        pygame.draw.ellipse(win,(255,255,255),(20,830,500,200))
        pygame.draw.ellipse(win,(0,0,0),(20,830,500,200),20)
        
        pygame.draw.ellipse(win,(255,255,255),(1200,400,500,200))
        pygame.draw.ellipse(win,(0,0,0),(1200,400,500,200),20)
        
        if animation_data["Type"]=="Transition Start":
            win.blit(player_sprite,(60,520))
            animation_data["Frames Left"]-=1
            dark_screen.set_alpha(int(255/72*animation_data["Frames Left"]))
            win.blit(dark_screen,(0,0))
            if animation_data["Frames Left"]==0:
                animation_data={
                    "Type":"Summoning Matheons",
                    "Frames Left":500,
                    "Pokeball X":320,
                    "Pokeball Y":700,
                    "Pokeball Velocity":[0.45,-8.5],
                    "Pokeball G Acceleration":0.21                   
                }
        if animation_data["Type"]=="Summoning Matheons":
            animation_data["Frames Left"]-=1
            if animation_data["Frames Left"]>400:
                animation_data["Pokeball Velocity"][1]+=animation_data["Pokeball G Acceleration"]
                animation_data["Pokeball Y"]+=animation_data["Pokeball Velocity"][1]
                animation_data["Pokeball X"]+=animation_data["Pokeball Velocity"][0]
                pygame.draw.polygon(win,(0,0,0),[
                    [animation_data["Pokeball X"]+cos(animation_data["Pokeball Y"]+tau/6*i)*(27-(i%2==1)*13)
                     ,animation_data["Pokeball Y"]+sin(animation_data["Pokeball Y"]+tau/6*i)*(27-(i%2==1)*13)]
                     for i in range(6)]
                    ,5)
                #pygame.draw.polygon(win,(0,0,0),[],5)
            if animation_data["Frames Left"]>440:
                win.blit(player_sprite,(60-480*(500-animation_data["Frames Left"])/60,520))
            if 380>=animation_data["Frames Left"]>280:
                alpha=(421-animation_data["Frames Left"])/100
                attacker.sprite.set_alpha(alpha*255)
                defender.sprite.set_alpha(alpha*255)
                win.blit(attacker.sprite,(1250,100))
                win.blit(defender.sprite,(70,530))
            if animation_data==280:
                animation_data={
                    "Type":"None"
                }
        if animation_data["Type"]=="None":
            win.blit(attacker.sprite,(1250,100))
            win.blit(defender.sprite,(70,530))
        screen.blit(pygame.transform.scale(win,screen.get_size()),(0,0))
        pygame.display.update()
#This is used for Matheon Testing
new_matheon1=Battle_Matheon("Cubican",1)
new_matheon2=Battle_Matheon("Cubican",1)

#new_matheon1.use_move("Brute Force")
#print(new_matheon2.taken_damage)