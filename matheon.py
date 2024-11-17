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
        self.new_defense=self.base_defense
        self.new_attack=self.base_attack
        self.new_health=self.base_max_health
        self.new_speed=self.base_speed
        self.sprite=pygame.transform.scale(pygame.image.load(self.data["Sprite Path"]),(400,400))
        self.display_health_surface=pygame.Surface((700,200))
        self.display_health_surface.set_colorkey((234,23,4))
        self.taken_damage=0
        self.taken_damage_frames_left=0
        self.if_statement_failed=False
    def use_move(self,move_name):
        self.if_statement_failed=False
        self.used_move=move_data[move_name]
        for action in self.used_move["Actions"]:
            self.do_action(action)
    def do_action(self,action):
        print(action)
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
                self.if_statement_failed=True
        if "Deal Damage" in action:
            self.enemy.deal_damage(self,action["Deal Damage"])
        if "Apply Effect" in action:
            if action["Apply Effect"]["Target"]=="Self":
                self.apply_effect(action["Apply Effect"]["Effect"])
            elif action["Apply Effect"]["Target"]=="Enemy":
                self.enemy.apply_effect(action["Apply Effect"]["Effect"])
    def deal_damage(self,attacker,how_much):
        self.taken_damage=attacker.new_attack*how_much*(2/3+random())/self.new_defense
        self.taken_damage_frames_left=100
        #print(self.taken_damage)
    def apply_effect(self,effect,by_who=None):
        if "Frail" in effect:
            self.new_defense*=1-effect["Frail"]
        if "Decay" in effect:
            self.new_speed*=1-effect["Delay"]
        if "Sap" in effect:
            self.new_attack*=1-effect["Sap"]
        if "Surge" in effect:
            self.new_attack*=1+effect["Surge"]
        if "Tough" in effect:
            self.new_defense*=1+effect["Tough"]
    def logarithmic_infinity_display(self,number):
        return number*100
    def draw_bar(self):
        if self.taken_damage_frames_left>0:
            self.new_health-=self.taken_damage/100
            self.taken_damage_frames_left-=1
        self.display_health_surface.fill((234,23,4))
        self.health_q=self.new_health/self.base_max_health
        pygame.draw.rect(self.display_health_surface,(200,200,200),(0,0,700,120),0,17)
        pygame.draw.rect(self.display_health_surface,(234,23,4),(20,10,660,60),0,15)
        pygame.draw.rect(self.display_health_surface,(255-255*self.health_q,255*self.health_q,4),(24,14,652*self.health_q,52),0,15)
        center(self.display_health_surface,render_text(self.type,size=23,color=(25,25,25)),70,100)
#class Button:
#    def __init__(self,text,color,x_size,y_size):
#        self.text=render_text(text,30)
        #self.sprite=pygame.Surface((self.text))
def Battle(controlled_by_player,attacked_player,win,screen):
    mouse_position_difference=[screen.get_size()[i]/win.get_size()[i] for i in range(2)]
    print(screen.get_size(),win.get_size())
    print(mouse_position_difference)
    defender=controlled_by_player
    attacker=attacked_player
    defender.enemy=attacker
    attacker.enemy=defender
    Button=[
        [pygame.image.load(i),625+250*I,1100,1100] for I,i in enumerate([
            "Resources/Sprites/Attack_button.png",
            "Resources/Sprites/Special_button.png",
            "Resources/Sprites/Items_button.png",
            "Resources/Sprites/Run_button.png",
        ])
    ]
    moves_learned=len(defender.known_moves)
    Attack_Buttons=[
        {
            "Text":render_text(i,30,(0,0,0)),
            "X Pos":(2000-(moves_learned-1)*250)/2+I*250,
            "Y Pos":1100,
            "Y Weight":1100,
            "Move":i
        } for I,i in enumerate(defender.known_moves)
    ]
    for i in Attack_Buttons:
        i["Button Size"]=[i["Text"].get_size()[ii]*1.2 for ii in range(2)]
        i["Button"]=pygame.Surface(i["Button Size"])
        i["Button"].set_colorkey((0,0,0))
        pygame.draw.rect(i["Button"],(172,172,172),(0,0,i["Button Size"][0],i["Button Size"][1]),0,12)
        center(i["Button"],i["Text"],i["Button Size"][0]/2,i["Button Size"][1]/2)
    menu="None (Startup)"


    run=True
    frame=0
    is_battle_screen_running=True
    clock=pygame.time.Clock()
    dark_screen=pygame.Surface((2000,1000))
    animation_data={
        "Type":"Transition Start",
        "Frames Left":72
        }
    click=[False,False,False]
    ctimer=[0,0,0]
    while run and is_battle_screen_running: #Mainloop
        frame+=1
        clock.tick(144)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        mouse_pos=pygame.mouse.get_pos()
        mouse_down=pygame.mouse.get_pressed()
        mouse_pos=[mouse_pos[i]/mouse_position_difference[i] for i in range(2)]
        ctimer=[(ctimer[i]+1)*int(mouse_down[i]) for i in range(3)]
        click=[ctimer[i]==1 for i in range(3)]
        if keys[27]: run=False
        win.fill((25,25,25))

        pygame.draw.ellipse(win,(255,255,255),(20,830,500,200))
        pygame.draw.ellipse(win,(0,0,0),(20,830,500,200),20)
        
        pygame.draw.ellipse(win,(255,255,255),(1200,400,500,200))
        pygame.draw.ellipse(win,(0,0,0),(1200,400,500,200),20)
        win.blit(attacker.sprite,(1250,100))
        pygame.draw.circle(win,(255,255,255),mouse_pos,10,2)
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
                menu="Main"
        if animation_data["Type"]=="None":
            win.blit(defender.sprite,(70,530))
            win.blit(defender.display_health_surface,(690,730))
        if menu=="Main":
            for BI,button in enumerate(Button):
                button[2]=(button[3]+button[2]*19)/20
                if abs(mouse_pos[0]-button[1])<90 and mouse_pos[1]>750:
                    button[3]=900
                    if click[0]:
                        if BI==0:
                            menu="Attack"
                            for BI,button in enumerate(Button):
                                button[3]=1100
                        elif BI==1:
                            menu="Main"
                            print("Not Implemented Yet")
                        elif BI==2:
                            menu="Main"
                            print("Not Implemented Yet")
                        elif BI==3:
                            is_battle_screen_running=False
                            return {
                                "Matheon Defeated":False
                            }
                elif menu=="Main":
                    button[3]=950
                center(win,button[0],button[1],button[2])
        if menu=="Attack":
            for BI,button in enumerate(Attack_Buttons):
                if abs(mouse_pos[0]-button["X Pos"])<90 and mouse_pos[1]>750:
                    button["Y Weight"]=900
                    if click[0]:
                        menu="Display Attack"
                        animation_data={
                            "Type":"Show F Message On Screen",
                            "Message":[f"{defender.type} used {button['Move']}"],
                            "After":{
                                "Type":"Use Move",
                                "Move":button["Move"],
                                "Screen State":"Display Enemy Attack"
                            }
                        }
                        for BI,button in enumerate(Attack_Buttons):
                            button["Y Weight"]=1100
                elif menu=="Attack":
                    button["Y Weight"]=950
        elif animation_data["Type"]=="Show F Message On Screen":
            
            pygame.draw.rect(win,(205,205,205),(0,800,2000,200),0,20)
            for I,i in enumerate(animation_data["Message"]):
                win.blit(render_text(str(i),color=(0,0,0)),(20,815+30*I))
            #pygame.draw.rect(win,(255,255,255),())
            #pygame.draw.rect(win,(255,255,0),())
            if click[0]:
                
                if animation_data["After"]["Type"]=="Use Move":
                    defender.use_move(animation_data["After"]["Move"])
                    if defender.if_statement_failed:
                        animation_data={
                                "Type":"Show F Message On Screen",
                                "Message":[animation_data["After"]["Move"]+" Failed"],
                                "After":{
                                    "Type":"Show Message",
                                    "Screen State":"Display Enemy Attack"
                                }
                            }
                    else:
                        menu=animation_data["After"]["Screen State"]
                        animation_data={
                            "Type":"None"
                        }
                else:
                    menu=animation_data["After"]["Screen State"]
                    animation_data={
                        "Type":"None"
                    }
        elif menu=="Display Enemy Attack":
            used_move=choice(attacker.known_moves)
            
            animation_data={
                            "Type":"Show E Message On Screen",
                            "Message":[f"Enemy {attacker.type} used {used_move}"],
                            "After":{
                                "Type":"Use Move",
                                "Move":used_move,
                                "Screen State":"Main"
                            }
                        }
            menu="Do Display Enemy Attack"
        elif animation_data["Type"]=="Show E Message On Screen":
            pygame.draw.rect(win,(205,205,205),(0,800,2000,200),0,20)
            for I,i in enumerate(animation_data["Message"]):
                win.blit(render_text(str(i),color=(0,0,0)),(20,815+30*I))
            #pygame.draw.rect(win,(255,255,255),())
            #pygame.draw.rect(win,(255,255,0),())
            if click[0]:
                
                if animation_data["After"]["Type"]=="Use Move":
                    attacker.use_move(animation_data["After"]["Move"])
                    if attacker.if_statement_failed:
                        animation_data={
                                "Type":"Show E Message On Screen",
                                "Message":["Enemy "+animation_data["After"]["Move"]+" Failed"],
                                "After":{
                                    "Type":"Show Message",
                                    "Screen State":"Main"
                                }
                            }
                    else:
                        menu=animation_data["After"]["Screen State"]
                        animation_data={
                            "Type":"None"
                        }
                else:
                    menu=animation_data["After"]["Screen State"]
                    animation_data={
                        "Type":"None"
                    }
        for button in Button:
            button[2]=(button[3]+button[2]*19)/20
            center(win,button[0],button[1],button[2])
        for button in Attack_Buttons:
            button["Y Pos"]=(button["Y Pos"]*19+button["Y Weight"])/20
            center(win,button["Button"],button["X Pos"],button["Y Pos"])
        screen.blit(pygame.transform.scale(win,screen.get_size()),(0,0))
        pygame.display.update()
        if attacker.new_health<=0:
            return "Victory"
        if defender.new_health<=0:
            return "Loss"
        
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