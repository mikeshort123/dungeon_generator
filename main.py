import pygame,json

from src.tile import Tile
from src.wfc import WFC
from src.biome import Biome

pygame.init()


temple = Biome("res/temple.json")
jungle = Biome("res/jungle.json")



Biome.generateAllTileRules()


SCREEN_SIZE = 750

W = 25
SCL = SCREEN_SIZE // W

screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])

wfc = WFC(W,SCL,temple,jungle)

updateList = []
for i in range(W): # add void border
    wfc.forceCollapse(updateList,wfc.grid,i,0,temple.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,i,W-1,temple.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,0,i,temple.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,W-1,i,temple.tileList["blank"])


img = [ # add spawn room
    ["room_corner_3","room_wall_3","room_corner_4"],
    ["room_door_2","room","room_door_4"],
    ["room_corner_2","room_door","room_corner"]
]
x,y = wfc.spawnx-1,wfc.spawny-1
for i in range(3):
    for j in range(3):
        wfc.forceCollapse(updateList,wfc.grid,x+i,y+j,temple.tileList[img[j][i]])

img = [ # add boss room
    ["room_corner_3","room_door_3","room_wall_3","room_door_3","room_corner_4"],
    ["room_door_2","room","room_chest","room","room_door_4"],
    ["room_corner_2","room_wall","room_wall","room_wall","room_corner"]
]
x,y = wfc.spawnx-2,W-3
for i in range(5):
    for j in range(3):
        wfc.forceCollapse(updateList,wfc.grid,x+i,y+j,temple.tileList[img[j][i]])

wfc.applyAllRules(wfc.grid,updateList)

wfc.go(screen)
grid = wfc.grid


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
