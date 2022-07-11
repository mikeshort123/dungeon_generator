import pygame,sys

from src.loader import Loader
from src.wfc import WFC
from src.processor import Processor

def main():

    pygame.init()

    map = Loader.loadWorld("res/world.json")

    SCL = 30
    screen = pygame.display.set_mode([map.W * SCL, map.H * SCL])




    wfc = WFC(drawFunction = getDrawFunction(screen,SCL))
    wfc.applyAllRules(map)

    # run WFC algorithm
    map = wfc.step(map)


    #p = Processor(map,"res/processing.json")
    #p.applyRules()
    #p.save("temple.grid")



    # leave screen open until close button is pressed
    while True:
        handlePygameExit()





def getDrawFunction(screen,SCL): # generate a function for drawing the partially completed grid to the screen

    def drawGrid(map):

        handlePygameExit()

        for cell in map.grid:
            x,y = cell.x,cell.y
            cell.render(screen,x*SCL,y*SCL,SCL)

        pygame.display.update()

    return drawGrid


def handlePygameExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)


if __name__ == "__main__": main()
