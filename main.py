import copy
import pygame

pygame.display.init()
window=pygame.display.set_mode((16*70,9*70))

class Tile:
    def __init__(self,imgpath) -> None:
        self.img=pygame.image.load("assets/"+imgpath).convert_alpha()
        self.x=0
        self.y=0

    def render(self,holding=False):
        if holding:
            img=pygame.transform.scale(self.img,(96,96))
            img.set_alpha(180)
            window.blit(img,((self.x*64)+((window.get_width()-96)/2),((self.y*64)+((window.get_height()-96)/2))))
            return
        window.blit(self.img,((self.x*64)+((window.get_width()-64)/2),((self.y*64)+((window.get_height()-64)/2))))

try:
    grass = Tile("grass.png")
except FileNotFoundError:
    raise NotImplementedError("This error message will be better.")


cursor=copy.copy(grass)


while True:
    EVENTS = pygame.event.get()
    for event in EVENTS:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.fill("#000000")

    grass.render()
    cursor.x=1
    cursor.render(True)

    pygame.display.flip()