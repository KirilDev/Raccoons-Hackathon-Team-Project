#Should handle mainly the standart stuff, visual stuff later. 
from map import *
with open("Resources/Misc/sight_map.json") as file:
    sight_data=json.loads(file.read())
class Entity:
    def __init__(self,type):
        self.type=type
        self.active=False
        self.x=0
        self.y=0
        self.z=0
        self.squares_seen=[]
        self.walls_seen=[]
        self.health_level=0
    def update_vision(self,heightmap):
        visible_tiles=set()
        checked_tiles=set()
        blocked_tiles=set()
        walls_seen=set()
        map_size=(len(heightmap[0]),len(heightmap))
        for i in sight_data["Order Of Checking"]:
            stri=str(i)
            if not stri in checked_tiles: #let's keep it as a heightmap, because it will get very convoluted very quickly 
                if not map_size[1]>self.z+i[2]>-1: #Several Break Chains to test out of bounds squares
                    break
                if not map_size[0]>self.x+i[0]>-1:
                    break
                #print(i,heightmap[self.z+i[2]][self.x+i[0]],self.x+i[0],self.z+i[2])
                if heightmap[self.z+i[2]][self.x+i[0]]>=self.y+i[1]+1: #The terrain is blocked
                    for ii in sight_data["Sight Map"][stri]:
                        blocked_tiles.add(str(ii))
                        checked_tiles.add(str(ii))
                    walls_seen.add(stri)
                elif heightmap[self.z+i[2]][self.x+i[0]]<=self.y+i[1]: #The Terrain isn't blocked
                    visible_tiles.add(stri)
                checked_tiles.add(stri)
        self.squares_seen=[[self.x,self.y,self.z]]+[[int(ii)+[self.x,self.y,self.z][II] for II,ii in enumerate(i[1:-1].split(","))] for i in visible_tiles]
        self.walls_seen=[[self.x,self.y,self.z]]+[[int(ii)+[self.x,self.y,self.z][II] for II,ii in enumerate(i[1:-1].split(","))] for i in walls_seen]
        self.squares_un_seen=[[int(ii)+[self.x,self.y,self.z][II] for II,ii in enumerate(i[1:-1].split(","))] for i in blocked_tiles]