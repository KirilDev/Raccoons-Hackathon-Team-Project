from entity import *
#unseen_surface=pygame.Surface((128,128))
#unseen_surface.set_alpha()
class Player:
    def __init__(self):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        self.display_x=self.entity.x
        self.display_z=self.entity.z
        self.state={}
        #self.discovered_surface(())
    def move(self,heightmap,direction):
        if direction=="Down":
            if self.entity.z<len(heightmap.heightmap)-1:
                if heightmap.heightmap[self.entity.z+1][self.entity.x]<=self.entity.y:
                    #self.entity.z+=1
                    self.state={
                        "Type":"Moving Animation",
                        "Direction":"Down",
                        "Frames Left":10
                    }
        if direction=="Up":
            if self.entity.z>0:
                if heightmap.heightmap[self.entity.z-1][self.entity.x]<=self.entity.y:
                    #self.entity.z-=1
                    self.state={
                        "Type":"Moving Animation",
                        "Direction":"Up",
                        "Frames Left":10
                    }
        if direction=="Right":
            if self.entity.x<len(heightmap.heightmap[0])-1:
                if heightmap.heightmap[self.entity.z][self.entity.x+1]<=self.entity.y:
                    self.entity.x+=1
                    self.state={
                        "Type":"Moving Animation",
                        "Direction":"Right",
                        "Frames Left":10
                    }
        if direction=="Left":
            if self.entity.x>0:
                if heightmap.heightmap[self.entity.z][self.entity.x-1]<=self.entity.y:
                    self.entity.x-=1
                    self.state={
                        "Type":"Moving Animation",
                        "Direction":"Left",
                        "Frames Left":10
                    }
        self.entity.update_vision(heightmap.heightmap)
    def update_state(self):
        if self.state!={}:
            if self.state["Type"]=="Moving Animation":
                self.state["Frames Left"]-=1
                if self.state["Direction"]=="Up":
                    self.display_z=self.entity.x-1+0.1*self.state["Frames Left"]
                if self.state["Direction"]=="Down":
                    self.display_z=self.entity.x+1-0.1*self.state["Frames Left"]
                
                if self.state["Frames Left"]==0:
                    if self.state["Direction"]=="Up":
                        self.entity.z-=1
                    if self.state["Direction"]=="Down":
                        self.entity.z+=1
                    self.display_x=self.entity.x
                    self.display_z=self.entity.z
                    self.state={}
            