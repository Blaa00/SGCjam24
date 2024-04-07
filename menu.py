import pygame
from util import *

def inMenu(window:pygame.Surface):
    while True:
        handleExit()

        window.fill("black")

        txtsurf=renderText("Roboto",45,"Spelare:","white")
        window.blit(txtsurf,(window.get_width()/2-txtsurf.get_width()/2,window.get_height()/2-txtsurf.get_height()))

        mouseX,mouseY=pygame.mouse.get_pos()
        for x in range(4):
            txtsurf=renderText("Roboto",30,f"{x+2}","white")
            rect=pygame.Rect(0,0,60,60)
            rect=rect.move(window.get_width()/2-rect.width/2+(x-1)*70-35,window.get_height()/2)
            pygame.draw.rect(window,["black","#555555"][rect.collidepoint(mouseX,mouseY)],rect)
            pygame.draw.rect(window,"white",rect,2,5)
            window.blit(txtsurf,rect.move(rect.w/2-txtsurf.get_width()/2,rect.h/2-txtsurf.get_height()/2))

            if rect.collidepoint(mouseX,mouseY) and pygame.mouse.get_pressed()[0]:
                return x+2


        pygame.display.flip()