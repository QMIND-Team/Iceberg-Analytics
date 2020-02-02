import pygame

pygame.init()

displayWidth = 800
displayHeight = 600
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
startedSim = False

windowDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption("Rebound Prediction")

rinkImg = pygame.image.load("./assets/HockeyRinkZone.png")
titleImg = pygame.image.load("./assets/titlePage.png")

def mainWindowLoop():
    while not startedSim:
        pygame.event.get()

        windowDisplay.blit(titleImg, (0,0))


mainWindowLoop()
pygame.quit()
quit()
