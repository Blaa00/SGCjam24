import os
import pygame
from util import *

def inMenu(window:pygame.Surface):
    clock = pygame.time.Clock()

    while True:
        dt=clock.tick(60)

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

        txtsurf=renderText("Roboto",30,f"Spelregler","white")
        rect=txtsurf.get_rect()
        rect=rect.inflate(20,20)
        rect=rect.move(window.get_width()/2-rect.width/2+10,window.get_height()/2+70+10)
        pygame.draw.rect(window,["black","#555555"][rect.collidepoint(mouseX,mouseY)],rect)
        pygame.draw.rect(window,"white",rect,2,5)
        window.blit(txtsurf,rect.move(rect.w/2-txtsurf.get_width()/2,rect.h/2-txtsurf.get_height()/2))
        if rect.collidepoint(mouseX,mouseY) and pygame.mouse.get_pressed()[0]:
            os.system(os.path.abspath("assets/rules.pdf"))


        pygame.display.flip()