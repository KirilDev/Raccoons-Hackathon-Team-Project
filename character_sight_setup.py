from math import *
#Lets say the screen is 15x15x7
import pygame
surface=pygame.Surface((15,15*7))
square_export={}
order_of_checking={}
for x in range(15): #15
    x-=7
    for z in range(15): #15
        z-=7
        for y in range(7): #7
            y-=3
            sum_of_xyz=abs(x)+abs(y)+abs(z)
            if sum_of_xyz>0:
                sight_dist=dist((0,0,0),(x,z,y*2))
                if sight_dist<8:
                    surface.set_at((x+7,z+7+(y+3)*15),(255,sight_dist/8*255,0))
                    if not sight_dist in order_of_checking:
                        order_of_checking[sight_dist]=[[x,y,z]]
                    else:
                        order_of_checking[sight_dist].append([x,y,z])
                    x_mod=x/sum_of_xyz/100*8
                    y_mod=y/sum_of_xyz/100*8
                    z_mod=z/sum_of_xyz/100*8
                    x_pos=0
                    y_pos=0
                    z_pos=0
                    squares_seen={(0,0,0)}
                    while not (x,y,z) in squares_seen:
                        x_pos+=x_mod
                        y_pos+=y_mod
                        z_pos+=z_mod
                        squares_seen.add((int(x_pos),int(y_pos),int(z_pos)))
                    if (int(x_pos),int(y_pos),int(z_pos))!=(x,y,z):
                        print(int(x_pos)-x,int(y_pos)-y,int(z_pos)-z)
                        print(squares_seen)
                        print((int(x_pos),int(y_pos),int(z_pos)),(x,y,z))
                        print(x_mod,y_mod,z_mod)
                        exit()
                    for i in squares_seen:
                        #print(i)
                        listi=list(i)
                        i=str(list(i))
                        if not f"[{x}, {y}, {z}]" in square_export:
                            square_export[f"[{x}, {y}, {z}]"]=[]
                        if listi!=[x,y,z]:
                            if not i in square_export:
                                square_export[i]=[[x,y,z]]
                            else:
                                square_export[i].append([x,y,z])
square_export={
    "Sight Map":square_export,
    "Order Of Checking":[]
}

for i in sorted(list(order_of_checking.keys())):
    for ii in order_of_checking[i]:
        square_export["Order Of Checking"].append(ii)
import json
with open("sight_map.json","w") as file:
    file.write(json.dumps(square_export,indent=4))
pygame.image.save(surface,"sight_map.png")