import pygame,json

from src.tile import Tile
from src.wfc import WFC

pygame.init()


f = open("res/tiles.json","r")
data = json.load(f)
f.close

for tile in data["tiles"]:
    Tile.loadTile(tile)

Tile.generateAllRules()


SCREEN_SIZE = 750

W = 25
SCL = SCREEN_SIZE // W

screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])

wfc = WFC(W,SCL)

updateList = []
for i in range(W): # add void border
    wfc.forceCollapse(updateList,wfc.grid,i,0,Tile.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,i,W-1,Tile.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,0,i,Tile.tileList["blank"])
    wfc.forceCollapse(updateList,wfc.grid,W-1,i,Tile.tileList["blank"])


img = [ # add spawn room
    ["room_corner_3","room_wall_3","room_corner_4"],
    ["room_door_2","room","room_door_4"],
    ["room_corner_2","room_door","room_corner"]
]
x,y = wfc.spawnx-1,wfc.spawny-1
for i in range(3):
    for j in range(3):
        wfc.forceCollapse(updateList,wfc.grid,x+i,y+j,Tile.tileList[img[j][i]])

img = [ # add boss room
    ["room_corner_3","room_door_3","room_wall_3","room_door_3","room_corner_4"],
    ["room_door_2","room","room_chest","room","room_door_4"],
    ["room_corner_2","room_wall","room_wall","room_wall","room_corner"]
]
x,y = wfc.spawnx-2,W-3
for i in range(5):
    for j in range(3):
        wfc.forceCollapse(updateList,wfc.grid,x+i,y+j,Tile.tileList[img[j][i]])

wfc.applyAllRules(wfc.grid,updateList)

wfc.go(screen)
grid = wfc.grid


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
