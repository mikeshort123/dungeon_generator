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

    wfc = WFC(W,SCL)

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
    x,y = wfc.spawnx-1,wfc.spawny-1
    map.drawImage(img,temple,x,y)

    img = [ # add boss room
        ["room_corner_3","room_door_3","room_wall_3","room_door_3","room_corner_4"],
        ["room_door_2","room","room_chest","room","room_door_4"],
        ["room_corner_2","room_wall","room_wall","room_wall","room_corner"]
    ]
    x,y = wfc.spawnx-2,W-3
    map.drawImage(img,temple,x,y)

    wfc.applyAllRules(map)

    map = wfc.step(map,screen)


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()

if __name__ == "__main__": main()
