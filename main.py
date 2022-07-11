import pygame,sys

from src.loader import Loader
from src.wfc import WFC
from src.processor import Processor

def main():

    pygame.init()

    # generate map
    map = Loader.loadWorld("res/world.json")

    # set up pygame display
    SCL = 30
    screen = pygame.display.set_mode([map.W * SCL, map.H * SCL])

    # run WFC algorithm to fill in map
    map = WFC.step(map, drawFunction = getDrawFunction(screen,SCL))

    # process map into version readable by a game
    p = Processor(map,"res/processing.json")
    p.applyRules()
    p.save("temple.grid")

    # leave screen open until close button is pressed
    while True:
        handlePygameExit()


def getDrawFunction(screen,SCL): # generate a function for drawing the partially completed grid to the screen

    def drawGrid(map):

        handlePygameExit()

        for cell in map.grid:

            x, y = cell.x*SCL, cell.y*SCL
            if cell.isCollapsed():
                tile = cell.getFinalOption()
                pw = SCL // tile.size

                for i in range(tile.size):
                    for j in range(tile.size):

                        c = tile.img[j][i].colour
                        pygame.draw.rect(screen,c,(x + i*pw, y + j*pw, pw,pw))

            else:
                c = 100
                pygame.draw.rect(screen,(c,c,c),(x,y,SCL,SCL))

        pygame.display.update()

    return drawGrid


def handlePygameExit(): # clear event queue and quit game if button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)


if __name__ == "__main__": main()
