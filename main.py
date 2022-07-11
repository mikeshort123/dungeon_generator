import pygame,sys

from src.wfc import WFC
from src.biome import Biome
from src.map import Map
from src.processor import Processor

def main():

    pygame.init()

    SCREEN_SIZE = 750
    W = 25
    SCL = SCREEN_SIZE // W
    screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])

    temple = Biome("res/biomes/temple.json")
    jungle = Biome("res/biomes/jungle.json")

    Biome.generateAllTileRules()


    startx,starty = W//2, 1 # start and end positions
    endx,endy = W//2, W-2

    distribution = [ # biome distribution, temple in certain radius from start and end, jungle elsewhere
        [temple if distCheck(i,j,startx,starty,7) or distCheck(i,j,endx,endy-1,9) else jungle for j in range(W)] for i in range(W)
    ]

    map = Map(W,distribution)



    # add some preset stuff to the dungeon

    #left/right walls
    map.drawImage([["blank"]] * W,jungle,0,0)
    map.drawImage([["blank"]] * W,jungle,W-1,0)
    #top wall
    map.drawImage([["blank"] * 4 + ["wall_straight_4"]] ,jungle,1,0)
    map.drawImage([["wall_straight_4"] + ["blank"] * 4],temple,6,0)
    map.drawImage([["blank"] * 4 + ["wall_straight_2"]],temple,14,0)
    map.drawImage([["wall_straight_2"] + ["blank"] * 4],jungle,19,0)
    #bottom wall
    map.drawImage([["blank"] * 2 + ["wall_straight_4"]] ,jungle,1,W-1)
    map.drawImage([["wall_straight_4"] + ["blank"] * 5],temple,4,W-1)
    map.drawImage([["blank"] * 5 + ["wall_straight_2"]],temple,15,W-1)
    map.drawImage([["wall_straight_2"] + ["blank"] * 2],jungle,21,W-1)


    img = [ # add spawn room
        ["room_corner_3","room_wall_3","room_corner_4"],
        ["room_door_2","room","room_door_4"],
        ["room_corner_2","room_door","room_corner"]
    ]
    map.drawImage(img,temple,startx-1,starty-1)

    img = [ # add boss room
        ["room_corner_3","room_door_3","room_wall_3","room_door_3","room_corner_4"],
        ["room_door_2","room","room_chest","room","room_door_4"],
        ["room_corner_2","room_wall","room_wall","room_wall","room_corner"]
    ]
    map.drawImage(img,temple,endx-2,endy-1)



    wfc = WFC(W, startx, starty, drawFunction = getDrawFunction(screen,SCL))
    wfc.applyAllRules(map)

    # run WFC algorithm
    map = wfc.step(map)


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
            x,y = cell.x,cell.y
            cell.render(screen,x*SCL,y*SCL,SCL)

        pygame.display.update()

    return drawGrid


def handlePygameExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)


def distCheck(x,y,ax,ay,r): # function for generating biome distributions

    return (x-ax) ** 2 + (y-ay) ** 2 < r ** 2


if __name__ == "__main__": main()
