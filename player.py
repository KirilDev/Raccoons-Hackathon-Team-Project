from entity import *
#unseen_surface=pygame.Surface((128,128))
#unseen_surface.set_alpha()
class Player:
    def __init__(self):
        self.entity=Entity("Pis Dirst")
        self.entity.active=True
        #self.discovered_surface(())
    def move(self,heightmap,direction):
        if direction=="Down":
            if self.entity.z<len(heightmap.heightmap)-1:
                if heightmap.heightmap[self.entity.z+1][self.entity.x]<=self.entity.y:
                    self.entity.z+=1
        if direction=="Up":
            if self.entity.z>0:
                if heightmap.heightmap[self.entity.z-1][self.entity.x]<=self.entity.y:
                    self.entity.z-=1
        if direction=="Right":
            if self.entity.x<len(heightmap.heightmap[0])-1:
                if heightmap.heightmap[self.entity.z][self.entity.x+1]<=self.entity.y:
                    self.entity.x+=1
        if direction=="Left":
            if self.entity.x>0:
                if heightmap.heightmap[self.entity.z][self.entity.x-1]<=self.entity.y:
                    self.entity.x-=1
        self.entity.update_vision(heightmap.heightmap)
