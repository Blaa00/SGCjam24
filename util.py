import pygame


def renderText(fontName, fontSize, text, color):
    font=pygame.font.SysFont(fontName, fontSize)
    return font.render(text,False,color)

def handleExit():
    EVENTS=pygame.event.get()
    for event in EVENTS:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    return EVENTS