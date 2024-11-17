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
        self.origin=self.data["Type"]
        self.known_moves=[]
        for i in self.data["Starting Moves"]:
            if i["Type"]=="Pool":
                self.known_moves+=sample(i["Possible Elements"],i["Selected Elements"])
        self.enemy=None
        self.new_deffense=self.base_defense
        self.new_attack=self.base_attack
        self.new_health=self.base_max_health
        self.new_speed=self.base_speed
        self.sprite=pygame.transform.scale(pygame.image.load(self.data["Sprite Path"]),(400,400))
        self.display_health_surface=pygame.Surface((700,200))
        self.display_health_surface.set_colorkey((234,23,4))
    def use_move(self,move_name):
        self.used_move=move_data[move_name]
        for action in self.used_move["Actions"]:
            self.do_action(action)
    def do_action(self,action):
        #print(action)
        if "If" in action:
            succesful_if=False
            if action["If"]["Type"]=="Random":
                if random()<action["If"]["Chance"]:
                    succesful_if=True
                    for nested_action in action["If"]["Then"]:
                        self.do_action(nested_action)
            if action["If"]["Type"]=="Check Type":
                if action["If"]["Target"]=="Enemy":
                    if self.enemy.origin==action["If"]["Test For Type"]:
                        succesful_if=True
                        for nested_action in action["If"]["Then"]:
                            self.do_action(nested_action)
            if not succesful_if:
                if "Else" in action["If"]:
                    for nested_action in action["If"]["Else"]:
                        self.do_action(nested_action)
        if "Deal Damage" in action:
            self.enemy.deal_damage(self,action["Deal Damage"])
        if "Apply Effect" in action:
            if action["Apply Effect"]["Target"]=="Self":
                self.apply_effect(action["Apply Effect"]["Effect"])
            elif action["Apply Effect"]["Target"]=="Enemy":
                self.enemy.apply_effect(action["Apply Effect"]["Effect"])
    def deal_damage(self,attacker,how_much):
        self.taken_damage=attacker.new_attack*how_much*(2/3+random())/self.new_defense
        self.new_health-=self.taken_damage
        #print(self.taken_damage)
    def apply_effect(self,effect,by_who=None):
        if "Frail" in effect:
            self.new_deffense*=1-effect["Frail"]
        if "Decay" in effect:
            self.new_speed*=1-effect["Delay"]
        if "Sap" in effect:
            self.new_attack*=1-effect["Sap"]
        if "Surge" in effect:
            self.new_attack*=1+effect["Surge"]
        if "Tough" in effect:
            self.new_attack*=1+effect["Tough"]
        
    def draw_bar(self):
        self.new_health-=0.1
        self.display_health_surface.fill((234,23,4))
        self.health_q=self.new_health/self.base_max_health
        pygame.draw.rect(self.display_health_surface,(200,200,200),(0,0,700,200),0,17)
        pygame.draw.rect(self.display_health_surface,(234,23,4),(20,10,660,60),0,15)
        pygame.draw.rect(self.display_health_surface,(255-255*self.health_q,255*self.health_q,4),(24,14,652*self.health_q,52),0,15)
        center(self.display_health_surface,render_text(self.type,size=23,color=(25,25,25)),70,100)
class Button:
    def __init__(self,text,color,x_size,y_size):
        self.text=render_text(text,30)
        #self.sprite=pygame.Surface((self.text))
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
        win.blit(attacker.sprite,(1250,100))
        defender.draw_bar()
        attacker.draw_bar()
        win.blit(attacker.display_health_surface,(450,30))
        if animation_data["Type"]=="Transition Start":
            win.blit(player_sprite,(60,520))
            animation_data["Frames Left"]-=1
            dark_screen.set_alpha(int(255/72*animation_data["Frames Left"]))
            win.blit(dark_screen,(0,0))
            if animation_data["Frames Left"]==0:
                animation_data={
                    "Type":"Summoning Matheons",
                    "Frames Left":500,
                    "Pokeball X":220,
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
                    [animation_data["Pokeball X"]+cos(animation_data["Pokeball Y"]/20+tau/6*i)*(27-(i%2==1)*6)
                     ,animation_data["Pokeball Y"]+sin(animation_data["Pokeball Y"]/20+tau/6*i)*(27-(i%2==1)*6)]
                     for i in range(6)]
                    ,5)
                #pygame.draw.polygon(win,(0,0,0),[],5)
            if animation_data["Frames Left"]>440:
                win.blit(player_sprite,(60-480*(500-animation_data["Frames Left"])/60,520))
            if 401>animation_data["Frames Left"]>370:
                pygame.draw.circle(win,(255,255,255),(270,870),20*1.2**(400-animation_data["Frames Left"]),12)
            if 395>=animation_data["Frames Left"]>295:
                alpha=(396-animation_data["Frames Left"])/100
                defender.sprite.set_alpha(alpha*255)
                win.blit(defender.sprite,(70,530))
            if animation_data["Frames Left"]==295:
                animation_data={
                    "Type":"None"
                }
        if animation_data["Type"]=="None":
            win.blit(defender.sprite,(70,530))
            win.blit(attacker.display_health_surface,(690,730))
            #pygame.draw.rect(win,(255,255,255),())
            #pygame.draw.rect(win,(255,255,0),())
        screen.blit(pygame.transform.scale(win,screen.get_size()),(0,0))
        pygame.display.update()
#This is used for Matheon Testing
new_matheon1=Battle_Matheon("Cubican",1)
new_matheon2=Battle_Matheon("Cubican",1)

#new_matheon1.use_move("Brute Force")
#print(new_matheon2.taken_damage)


# Brute
# L-hopital
# 
#
#
#