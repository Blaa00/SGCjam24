import copy
from enum import Enum, auto
import math
import random
import pygame

pygame.display.init()
window=pygame.display.set_mode((16*70,9*70))

pygame.font.init()

def renderText(fontName, fontSize, text, color):
    font=pygame.font.SysFont(fontName, fontSize)
    return font.render(text,False,color)

def handleExit():
    for event in EVENTS:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



class EDGES(Enum):
    grass=auto()
    river=auto()

class Tile:
    def __init__(self,imgpath,right=EDGES.grass,left=EDGES.grass,top=EDGES.grass,bottom=EDGES.grass) -> None:
        self.rotations=[top,right,bottom,left]
        #self.right=right
        #self.left=left
        #self.top=top
        #self.bottom=bottom

        self.img=pygame.transform.scale(pygame.image.load("assets/"+imgpath).convert_alpha(),(64,64))
        self.x=0
        self.y=0
    
    def getTop(self,rotation):
        return self.rotations[(0-rotation)%len(self.rotations)]
    def getRight(self,rotation):
        return self.rotations[(1-rotation)%len(self.rotations)]
    def getBottom(self,rotation):
        return self.rotations[(2-rotation)%len(self.rotations)]
    def getLeft(self,rotation):
        return self.rotations[(3-rotation)%len(self.rotations)]

    def render(self,x,y,rotation,offsetSeed,holding=False):
        if holding:
            img=pygame.transform.rotate(pygame.transform.scale(self.img,(96,96)),-rotation*90)
            img.set_alpha(180)
            window.blit(img,((x*70)+((window.get_width()-96)/2),((y*70)+((window.get_height()-96)/2))))
            return
        random.seed(offsetSeed)
        
        pos=((x*70)+((window.get_width()-64)/2)+random.randint(-2,2),((y*70)+((window.get_height()-64)/2))+random.randint(-2,2))
        window.blit(pygame.transform.rotate(self.img,-rotation*90),pos)
        window.blit(tileShadowImg,pos)


def selectTile(tiles:list|Tile):
    if type(tiles)==list:
        return random.choice(tiles)
    else:
        return tiles

def selectTiles(river=False):
    array=[]
    selectableTiles=defaultTiles
    if river:
        selectableTiles=riverTiles
    for i in selectableTiles:
        if type(i)==list:
            array+=i
        else:
            array.append(i)
    return random.choice(array)

try:
    tileShadowImg=pygame.image.load("assets/shadow.png").convert_alpha()

    grass = Tile("grass.png")
    riversStraight = [Tile("riverLR.png",EDGES.river,EDGES.river),Tile("riverLR1.png",EDGES.river,EDGES.river),Tile("riverLR2.png",EDGES.river,EDGES.river),Tile("riverLR3.png",EDGES.river,EDGES.river)]
    riversTurn = [Tile("riverLB.png",left=EDGES.river,bottom=EDGES.river)]
    riversEnd = Tile("riverL.png",left=EDGES.river)

    riverTiles=[riversStraight,riversTurn,riversEnd]
    defaultTiles=[]
except FileNotFoundError:
    txtsurf=renderText("Roboto",30,"Failed loading textures.","#ffffff")
    window=pygame.display.set_mode((txtsurf.get_width(),txtsurf.get_height()))
    pygame.display.set_caption("Error")
    window.blit(txtsurf,(0,0))
    pygame.display.flip()
    while True:
        EVENTS = pygame.event.get()
        handleExit()


cursor:Tile=selectTiles(river=True)
cursorRotation=0



lastKeysPressed=[]



clock = pygame.time.Clock()


world = {"0,0":[selectTile(riversStraight),random.randint(0,100),0]}



while True:
    dt = clock.tick(60)


    EVENTS = pygame.event.get()
    handleExit()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_r]:
        if not pygame.K_r in lastKeysPressed:
            cursorRotation+=1
            cursorRotation%=4
            lastKeysPressed.append(pygame.K_r)
    else:
        if pygame.K_r in lastKeysPressed:
            del lastKeysPressed[lastKeysPressed.index(pygame.K_r)]







    window.fill("#000000")

    
    for pos, info in world.items():
        info[0].render(int(pos.split(",")[0]),int(pos.split(",")[1]),info[2],info[1])

    cx=int((pygame.mouse.get_pos()[0]+35-window.get_width()/2)//70)
    cy=int((pygame.mouse.get_pos()[1]+35-window.get_height()/2)//70)
    if pygame.mouse.get_pressed()[0]:
        if not f"{cx},{cy}" in world:
            infoLeft=world.get(f"{cx-1},{cy}")
            infoRight=world.get(f"{cx+1},{cy}")
            infoTop=world.get(f"{cx},{cy-1}")
            infoBottom=world.get(f"{cx},{cy+1}")

            allow=True
            if infoLeft==None and infoRight==None and infoTop==None and infoBottom==None:allow=False

            if infoLeft:blockLeft:Tile=infoLeft[0]
            if infoRight:blockRight:Tile=infoRight[0]
            if infoTop:blockTop:Tile=infoTop[0]
            if infoBottom:blockBottom:Tile=infoBottom[0]

            if allow:
                if infoLeft:
                    if blockLeft.getRight(infoLeft[2])!=cursor.getLeft(cursorRotation):allow=False
                if infoTop:
                    if blockTop.getBottom(infoTop[2])!=cursor.getTop(cursorRotation):allow=False
                if infoRight:
                    if blockRight.getLeft(infoRight[2])!=cursor.getRight(cursorRotation):allow=False
                if infoBottom:
                    if blockBottom.getTop(infoBottom[2])!=cursor.getBottom(cursorRotation):allow=False

            if allow:
                if EDGES.river in cursor.rotations:
                    riverfound=False
                    if infoLeft:
                        if blockLeft.getRight(infoLeft[2])==EDGES.river:riverfound=True
                    if infoTop:
                        if blockTop.getBottom(infoTop[2])==EDGES.river:riverfound=True
                    if infoRight:
                        if blockRight.getLeft(infoRight[2])==EDGES.river:riverfound=True
                    if infoBottom:
                        if blockBottom.getTop(infoBottom[2])==EDGES.river:riverfound=True
                    if not riverfound:allow=False

            if allow:
                world[f"{cx},{cy}"]=[cursor,random.randint(0,100),cursorRotation]
                cursor=selectTiles(river=True)
    

    cursor.render(cx,cy,cursorRotation,0,True)

    window.blit(renderText("Roboto",30,f"FPS: {round(clock.get_fps())}", "#ff0000"),(5,5))
    pygame.display.flip()