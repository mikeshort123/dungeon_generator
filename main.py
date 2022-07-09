import pygame,json

from src.wfc import WFC
from src.biome import Biome
from src.map import Map

def main():

    pygame.init()

    SCREEN_SIZE = 750
    W = 25
    SCL = SCREEN_SIZE // W
    screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])

    temple = Biome("res/temple.json")
    jungle = Biome("res/jungle.json")

    Biome.generateAllTileRules()

    distribution = [[jungle if j < W//2 else temple for j in range(W)] for i in range(W)]

    map = Map(W,distribution)

    spawnx,spawny = W//2, 1

    wfc = WFC(W,spawnx,spawny,getDrawFunction(screen,SCL))


    # add some preset stuff to the dungeon

    for i in range(W): # add void border
        map.collapseCell(i,0,temple.tileList["blank"])
        map.collapseCell(i,W-1,temple.tileList["blank"])
        map.collapseCell(0,i,temple.tileList["blank"])
        map.collapseCell(W-1,i,temple.tileList["blank"])


    img = [ # add spawn room
        ["room_corner_3","room_wall_3","room_corner_4"],
        ["room_door_2","room","room_door_4"],
        ["room_corner_2","room_door","room_corner"]
    ]
    x,y = spawnx-1,spawny-1
    map.drawImage(img,temple,x,y)

    img = [ # add boss room
        ["room_corner_3","room_door_3","room_wall_3","room_door_3","room_corner_4"],
        ["room_door_2","room","room_chest","room","room_door_4"],
        ["room_corner_2","room_wall","room_wall","room_wall","room_corner"]
    ]
    x,y = spawnx-2,W-3
    map.drawImage(img,temple,x,y)

    wfc.applyAllRules(map)

    # run WFC algorithm
    map = wfc.step(map)


    # leave screen open until close button is pressed
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()


def getDrawFunction(screen,SCL): # generate a function for drawing the partially completed grid to the screen

    def drawGrid(map):

        pygame.event.pump() # gotta clear the event list every now and then...

        for cell in map.grid:
            x,y = cell.x,cell.y
            cell.render(screen,x*SCL,y*SCL,SCL)

        pygame.display.update()

    return drawGrid


if __name__ == "__main__": main()
