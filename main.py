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
    road=auto()

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
            img=pygame.transform.rotate(pygame.transform.scale(self.img,(80,80)),-rotation*90)
            img.set_alpha(180)
            pos=((x*70)+((window.get_width()-80)/2),((y*70)+((window.get_height()-80)/2)))
            window.blit(img,pos)
            window.blit(pygame.transform.scale(tileShadowImg,(80,80)),pos)
            return
        #random.seed(offsetSeed)
        
        pos=((x*70)+((window.get_width()-64)/2)+random.randint(-0,0),((y*70)+((window.get_height()-64)/2))+random.randint(-0,0))
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


def calculateRoadConnections(pos:tuple[int,int],fromTile:tuple[int,int]=None,road:list[tuple[int,int]]=None):
    x,y=pos
    if fromTile==None:fromTile=pos
    if road==None:road=[]


    roadConnections=0
    for i in world[(x,y)].tile.rotations:
        if i==EDGES.road:
            roadConnections+=1



    if road==[]:
        if roadConnections>2:
            if world[(x,y)].tile.getTop(world[(x,y)].rotation)==EDGES.road:
                if world.get((x,y-1)):
                    road.append(calculateRoadConnections((x,y-1)))

            if world[(x,y)].tile.getBottom(world[(x,y)].rotation)==EDGES.road:
                if world.get((x,y+1)):
                    road.append(calculateRoadConnections((x,y+1)))

            if world[(x,y)].tile.getLeft(world[(x,y)].rotation)==EDGES.road:
                if world.get((x-1,y)):
                    road.append(calculateRoadConnections((x-1,y)))

            if world[(x,y)].tile.getRight(world[(x,y)].rotation)==EDGES.road:
                if world.get((x+1,y)):
                    road.append(calculateRoadConnections((x+1,y)))

            return road
    
    a=None
    if fromTile[0]>pos[0]:
        a="r"
    elif fromTile[0]<pos[0]:
        a="l"
    elif fromTile[1]>pos[1]:
        a="d"
    elif fromTile[1]<pos[1]:
        a="u"
    if a:
        road.append([pos,a])
    else:
        road.append([pos])
    
    #if len(road)>1:
        #pos2=road[len(road)-2][0]
        #if fromTile[0]<pos2[0]:
        #    a="r"
        #elif fromTile[0]>pos2[0]:
        #    a="l"
        #elif fromTile[1]<pos2[1]:
        #    a="d"
        #elif fromTile[1]>pos2[1]:
        #    a="u"
        #road[len(road)-2].append(a)

    
    if roadConnections!=2:
        if len(road)>1:return road
    
    if not fromTile[1]<pos[1]:
        if world[(x,y)].tile.getTop(world[(x,y)].rotation)==EDGES.road:
            road[len(road)-1].append("u")
            if world.get((x,y-1)):
                road=calculateRoadConnections((x,y-1),pos,road)
                
    if not fromTile[1]>pos[1]:
        if world[(x,y)].tile.getBottom(world[(x,y)].rotation)==EDGES.road:
            road[len(road)-1].append("d")
            if world.get((x,y+1)):
                road=calculateRoadConnections((x,y+1),pos,road)

    if not fromTile[0]<pos[0]:
        if world[(x,y)].tile.getLeft(world[(x,y)].rotation)==EDGES.road:
            road[len(road)-1].append("l")
            if world.get((x-1,y)):
                road=calculateRoadConnections((x-1,y),pos,road)

    if not fromTile[0]>pos[0]:
        if world[(x,y)].tile.getRight(world[(x,y)].rotation)==EDGES.road:
            road[len(road)-1].append("r")
            if world.get((x+1,y)):
                road=calculateRoadConnections((x+1,y),pos,road)
    
    return road

def giveRoadScore(road):
    markers={}
    endsFound=0
    for tile in road:
        
        pos=tile[0]#pos, not direction
        if world[pos].player:
            if ["u","r","d","l"][world[pos].player[1]] in tile:
                if not world[pos].player[0] in markers: markers[world[pos].player[0]]=0
                markers[world[pos].player[0]]+=1
        roadEdges=0
        for edge in world[pos].tile.rotations:
            if edge in [EDGES.road]:
                roadEdges+=1
        if roadEdges!=2:
            endsFound+=1
    highest=0
    mostPlayers=[]
    for k,v in markers.items():
        if v>highest:
            mostPlayers=[k]
            highest=v
        elif v==highest:
            mostPlayers.append(k)
    if endsFound==2:
        for i in mostPlayers:
            playerScores[i]+=len(road)


def checkAirportScores(pos,_=False):
    x,y=pos
    x-=1
    y-=1
    score=1
    for x2 in range(3):
        x3=x+x2
        for y2 in range(3):
            y3=y+y2
            if (x3,y3)!=pos:
                if world.get((x3,y3)):
                    score+=1
                    if world[(x3,y3)].tile in airports:
                        checkAirportScores((x3,y3),True)
    if world[pos].tile in airports:
        if world[pos].player:
            if score == 9:
                playerScores[world[pos].player[0]]+=9



try:
    tileShadowImg=pygame.image.load("assets/shadow.png").convert_alpha()

    grass = Tile("grass.png")
    riversStraight = [Tile("riverLR.png",EDGES.river,EDGES.river),Tile("riverLR1.png",EDGES.river,EDGES.river),Tile("riverLR2.png",EDGES.river,EDGES.river),Tile("riverLR3.png",EDGES.river,EDGES.river),Tile("riverLRRoadTB.png",left=EDGES.river,right=EDGES.river,top=EDGES.road,bottom=EDGES.road),Tile("riverLR2RoadTB.png",left=EDGES.river,right=EDGES.river,top=EDGES.road,bottom=EDGES.road),Tile("riverLR3RoadTB.png",left=EDGES.river,right=EDGES.river,top=EDGES.road,bottom=EDGES.road)]
    riversTurn = [Tile("riverLB.png",left=EDGES.river,bottom=EDGES.river),Tile("riverLBRoadTR.png",left=EDGES.river,bottom=EDGES.river,top=EDGES.road,right=EDGES.road)]
    riversEnd = [Tile("riverL.png",left=EDGES.river)]*5

    roadsStraight = [Tile("roadLR.png",left=EDGES.road,right=EDGES.road),Tile("roadLR1.png",left=EDGES.road,right=EDGES.road),Tile("roadLR2.png",left=EDGES.road,right=EDGES.road)]
    roadsCrossings = [Tile("roadTRLB.png",EDGES.road,EDGES.road,EDGES.road,EDGES.road)]
    roadsTurn = [Tile("roadLB.png",left=EDGES.road,bottom=EDGES.road),Tile("roadLB1.png",left=EDGES.road,bottom=EDGES.road),Tile("roadLB2.png",left=EDGES.road,bottom=EDGES.road)]
    roadsEnd = [Tile("roadL.png",left=EDGES.road),Tile("roadL1.png",left=EDGES.road)]

    airports = [Tile("airport.png")]

    riverTiles=[riversStraight,riversTurn,riversEnd]
    defaultTiles=[roadsStraight,roadsCrossings,roadsEnd,roadsTurn,airports]
except FileNotFoundError:
    txtsurf=renderText("Roboto",30,"Failed loading textures.","#ffffff")
    window=pygame.display.set_mode((txtsurf.get_width(),txtsurf.get_height()))
    pygame.display.set_caption("Error")
    window.blit(txtsurf,(0,0))
    pygame.display.flip()
    while True:
        EVENTS = pygame.event.get()
        handleExit()


class Block:
    def __init__(self,tile:Tile,offsetSeed:int,rotation:int) -> None:
        self.tile=tile
        self.offsetSeed=offsetSeed
        self.rotation=rotation
        self.player=None


class World:
    def __init__(self) -> None:
        self._world={(0,0):Block(selectTile(riversStraight),random.randint(0,100),0)}
    
    def __getitem__(self, pos:tuple[int,int]):
        return self._world[pos]

    def __setitem__(self, key, value):
        self._world[key] = value

    def __delitem__(self, key):
        del self._world[key]

    def __iter__(self):
        return iter(self._world)

    def __len__(self):
        return len(self._world)
    
    def items(self):
        return self._world.items()
    
    def get(self,pos:tuple[int,int]):
        return self._world.get(pos)




cursor:Tile=selectTiles(river=True)
cursorRotation=0
placedRiverEnds=0


players=3
playerColors=["red","green","blue","black","yellow"]
currentTurn=0
playerScores=[]
for i in range(players):
    playerScores.append(0)
playerIsPlacingMarker=False



lastKeysPressed=[]



clock = pygame.time.Clock()


world = World()





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
        x,y=pos
        pos2=((x*70)+((window.get_width()-64)/2)+random.randint(-0,0),((y*70)+((window.get_height()-64)/2))+random.randint(-0,0))
        info.tile.render(int(pos[0]),int(pos[1]),info.rotation,info.offsetSeed)
        if info.player:
            if info.player[1]==-1:
                pygame.draw.circle(window,playerColors[info.player[0]],(pos2[0]+32,pos2[1]+32),10)
            elif info.player[1]==0:
                pygame.draw.circle(window,playerColors[info.player[0]],(pos2[0]+32,pos2[1]),10)
            elif info.player[1]==2:
                pygame.draw.circle(window,playerColors[info.player[0]],(pos2[0]+32,pos2[1]+64),10)
            elif info.player[1]==3:
                pygame.draw.circle(window,playerColors[info.player[0]],(pos2[0],pos2[1]+32),10)
            elif info.player[1]==1:
                pygame.draw.circle(window,playerColors[info.player[0]],(pos2[0]+64,pos2[1]+32),10)


    mouseX=pygame.mouse.get_pos()[0]
    mouseY=pygame.mouse.get_pos()[1]
    cx=int((mouseX+35-window.get_width()/2)//70)
    cy=int((mouseY+35-window.get_height()/2)//70)



    if playerIsPlacingMarker:
        x,y=playerIsPlacingMarker[0],playerIsPlacingMarker[1]
        pos=((x*70)+((window.get_width()-64)/2)+random.randint(-0,0),((y*70)+((window.get_height()-64)/2))+random.randint(-0,0))
        if world[playerIsPlacingMarker].tile in airports:
            #airport
            pygame.draw.circle(window,playerColors[currentTurn%players],(pos[0]+32,pos[1]+32),10)

        else:
            #road
            diffX=pos[0]+32-mouseX
            diffY=pos[1]+32-mouseY

            roadConnections=calculateRoadConnections(playerIsPlacingMarker)
            placeableDirections={"r":True,"d":True,"l":True,"u":True}
            if type(roadConnections[0][0])==list:
                #intersection
                for i in roadConnections:
                    for j in i:
                        if j[0]==playerIsPlacingMarker:
                            placeableDirections[j[1]]=True
                            for k in i:
                                if world[k[0]].player:
                                    placeableDirections[j[1]]=False
                                    
                            break
            

            if diffX<diffY and -diffX<diffY and world[playerIsPlacingMarker].tile.getTop(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["u"]: #up
                pygame.draw.circle(window,playerColors[currentTurn%players],(pos[0]+32,pos[1]),10)
            elif diffX>diffY and -diffX>diffY and world[playerIsPlacingMarker].tile.getBottom(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["d"]: #down
                pygame.draw.circle(window,playerColors[currentTurn%players],(pos[0]+32,pos[1]+64),10)
            elif diffX>diffY and diffX>-diffY and world[playerIsPlacingMarker].tile.getLeft(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["l"]: #left
                pygame.draw.circle(window,playerColors[currentTurn%players],(pos[0],pos[1]+32),10)
            elif diffX<diffY and diffX<-diffY and world[playerIsPlacingMarker].tile.getRight(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["r"]: #right
                pygame.draw.circle(window,playerColors[currentTurn%players],(pos[0]+64,pos[1]+32),10)
        
    if pygame.mouse.get_pressed()[0]:
        if not lmbPressed:
            lmbPressed=True
            if playerIsPlacingMarker:
                if world[playerIsPlacingMarker].tile in airports:
                    currentTurn+=1
                    world[playerIsPlacingMarker].player=[(currentTurn-1)%players,-1]#playernr, middle
                    checkAirportScores(playerIsPlacingMarker)
                    playerIsPlacingMarker=False
                else:
                    playerplacedmarkerpos=playerIsPlacingMarker
                    currentTurn+=1
                    if diffX<diffY and -diffX<diffY and world[playerIsPlacingMarker].tile.getTop(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["u"]:
                        world[playerIsPlacingMarker].player=[(currentTurn-1)%players,0]#playernr, top
                        playerIsPlacingMarker=False
                    elif diffX>diffY and -diffX>diffY and world[playerIsPlacingMarker].tile.getBottom(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["d"]:
                        world[playerIsPlacingMarker].player=[(currentTurn-1)%players,2]#playernr, bottom
                        playerIsPlacingMarker=False
                    elif diffX>diffY and diffX>-diffY and world[playerIsPlacingMarker].tile.getLeft(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["l"]:
                        world[playerIsPlacingMarker].player=[(currentTurn-1)%players,3]#playernr, left
                        playerIsPlacingMarker=False
                    elif diffX<diffY and diffX<-diffY and world[playerIsPlacingMarker].tile.getRight(world[playerIsPlacingMarker].rotation) in [EDGES.road] and placeableDirections["r"]:
                        world[playerIsPlacingMarker].player=[(currentTurn-1)%players,1]#playernr, right
                        playerIsPlacingMarker=False
                    else:
                        currentTurn-=1


                    #calculate score
                    roadConnections=calculateRoadConnections(playerplacedmarkerpos)
                    if type(roadConnections[0][0])==list:#intersection
                        for road in roadConnections:
                            giveRoadScore(road)
                    else:
                        giveRoadScore(roadConnections)

            else:
                if not (cx,cy) in world:
                    infoLeft=world.get((cx-1,cy))
                    infoRight=world.get((cx+1,cy))
                    infoTop=world.get((cx,cy-1))
                    infoBottom=world.get((cx,cy+1))

                    allow=True
                    if infoLeft==None and infoRight==None and infoTop==None and infoBottom==None:allow=False

                    if infoLeft:blockLeft:Tile=infoLeft.tile
                    if infoRight:blockRight:Tile=infoRight.tile
                    if infoTop:blockTop:Tile=infoTop.tile
                    if infoBottom:blockBottom:Tile=infoBottom.tile

                    if allow:
                        if infoLeft:
                            if blockLeft.getRight(infoLeft.rotation)!=cursor.getLeft(cursorRotation):allow=False
                        if infoTop:
                            if blockTop.getBottom(infoTop.rotation)!=cursor.getTop(cursorRotation):allow=False
                        if infoRight:
                            if blockRight.getLeft(infoRight.rotation)!=cursor.getRight(cursorRotation):allow=False
                        if infoBottom:
                            if blockBottom.getTop(infoBottom.rotation)!=cursor.getBottom(cursorRotation):allow=False

                    if allow:
                        if EDGES.river in cursor.rotations:
                            riverfound=False
                            if infoLeft:
                                if blockLeft.getRight(infoLeft.rotation)==EDGES.river:riverfound=True
                            if infoTop:
                                if blockTop.getBottom(infoTop.rotation)==EDGES.river:riverfound=True
                            if infoRight:
                                if blockRight.getLeft(infoRight.rotation)==EDGES.river:riverfound=True
                            if infoBottom:
                                if blockBottom.getTop(infoBottom.rotation)==EDGES.river:riverfound=True
                            if not riverfound:allow=False

                    if allow:
                        world[(cx,cy)]=Block(cursor,random.randint(0,100),cursorRotation)
                        checkAirportScores((cx,cy))
                        if cursor in riversEnd:
                            placedRiverEnds+=1
                        if placedRiverEnds>=2:
                            cursor=selectTiles()
                        else:
                            cursor=selectTiles(river=True)
                        

                        def allowPlaceMarker():
                            if world[(cx,cy)].tile in airports:
                                return True
                            else:
                                if EDGES.road in world[(cx,cy)].tile.rotations:
                                    connections=calculateRoadConnections((cx,cy),road=[])
                                    if type(connections[0][0])==list:
                                        pass
                                    else:
                                        for pos in connections:
                                            if world[pos[0]].player:
                                                if ["u","r","d","l"][world[pos[0]].player[1]] in pos:
                                                    return False
                                    return True
                                return False
                        
                        if not allowPlaceMarker():
                            #calculate score
                            roadConnections=calculateRoadConnections((cx,cy))
                            if type(roadConnections[0][0])==list:#intersection
                                for road in roadConnections:
                                    giveRoadScore(road)
                            else:
                                giveRoadScore(roadConnections)
                            currentTurn+=1
                        else:
                            playerIsPlacingMarker=(cx,cy)
    
    else:
        lmbPressed=False
                
            
    
    if not playerIsPlacingMarker:
        cursor.render(cx,cy,cursorRotation,0,True)



    pygame.draw.rect(window,playerColors[currentTurn%players],(0,window.get_height()-100,window.get_width(),100))


    txtsurf=renderText("Roboto",30,f"FPS: {round(clock.get_fps())}", "#ff0000")
    window.blit(txtsurf,(window.get_width()-txtsurf.get_width()-5,5))
    y=5
    for player, score in enumerate(playerScores):
        txtsurf=renderText("Roboto",25,f"{score} Poäng", playerColors[player])
        window.blit(txtsurf,(5,y))
        y+=txtsurf.get_height()
    pygame.display.flip()