import copy
from enum import Enum, auto
import pygame

pygame.display.init()
window=pygame.display.set_mode((16*70,9*70))

class EDGES(Enum):
    grass=auto()

class Tile:
    def __init__(self,imgpath,right=EDGES.grass,left=EDGES.grass,top=EDGES.grass,bottom=EDGES.grass) -> None:
        self.img=pygame.transform.scale(pygame.image.load("assets/"+imgpath).convert_alpha(),(64,64))
        self.x=0
        self.y=0

    def render(self,x,y,holding=False):
        if holding:
            img=pygame.transform.scale(self.img,(96,96))
            img.set_alpha(180)
            window.blit(img,((x*64)+((window.get_width()-96)/2),((y*64)+((window.get_height()-96)/2))))
            return
        window.blit(self.img,((x*64)+((window.get_width()-64)/2),((y*64)+((window.get_height()-64)/2))))

try:
    grass = Tile("grass.png")
except FileNotFoundError:
    raise NotImplementedError("This error message will be better.")


cursor=grass


world = {"0,0":grass}

while True:
    EVENTS = pygame.event.get()
    for event in EVENTS:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.fill("#000000")

    
    for pos, tile in world.items():
        tile.render(int(pos.split(",")[0]),int(pos.split(",")[1]))

    cx=int((pygame.mouse.get_pos()[0]+32-window.get_width()/2)//64)
    cy=int((pygame.mouse.get_pos()[1]+32-window.get_height()/2)//64)
    if pygame.mouse.get_pressed()[0]:
        if not f"{cx},{cy}" in world:
            blockLeft=world.get(f"{cx-1},{cy}")
            blockRight=world.get(f"{cx+1},{cy}")
            blockTop=world.get(f"{cx},{cy-1}")
            blockBottom=world.get(f"{cx},{cy+1}")

            allow=True
            if blockLeft==None and blockRight==None and blockTop==None and blockBottom==None:allow=False

            if allow:
                world[f"{cx},{cy}"]=cursor

    cursor.render(cx,cy,True)

    pygame.display.flip()