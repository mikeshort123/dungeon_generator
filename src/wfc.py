import pygame, random
from src.cell import Cell
from src.tile import Tile

class WFC:

    def __init__(self,W,SCL,temple,jungle):

        self.spawnx = 12
        self.spawny = 1

        self.W = W
        self.SCL = SCL

        self.finished = False

        self.grid = []

        for j in range(self.W):
            if j > self.W//2:
                b = jungle
            else:
                b = temple
            for i in range(self.W):

                self.grid.append(Cell(i,j,biome=b))




    def forceCollapse(self,updateList,grid,x,y,tile):

        cell = grid[self.index(x,y)]
        cell.collapse(tile)
        if cell not in updateList: updateList.append(cell)


    def go(self,screen):

        self.grid = self.step(self.grid,screen)
        return self.grid


    def step(self,grid,screen):

        lowest = self.getLowestEntropy(grid)

        if len(lowest) == 0: # no more un-collapsed cells, grid is done, return true
            return grid

        cell = random.choice(lowest)
        x, y = cell.x, cell.y

        if len(cell.options) == 0: # if no available picks, backtrack
            return None

        options = cell.options.copy()
        random.shuffle(options)
        for option in options: # try out each option (in a random order)

            next_grid = grid.copy()

            new_cell = Cell(x,y)
            new_cell.collapse(option)

            next_grid[self.index(x,y)] = new_cell

            self.applyAllRules(next_grid,[new_cell])

            if self.spawnWalk(next_grid,self.spawnx,self.spawny):

                self.drawGrid(next_grid,screen)

                p_grid = self.step(next_grid,screen)
                if p_grid:
                    return p_grid

        return None


    def applyAllRules(self,grid,applyStack):

        for cell in applyStack:


            x = cell.x
            y = cell.y

            dirList = [
                ["UP",    0,-1],
                ["DOWN",  0, 1],
                ["LEFT", -1, 0],
                ["RIGHT", 1, 0]
            ]

            for dir,dx,dy in dirList:
                nx,ny = x+dx, y+dy
                i = self.index(nx,ny)

                if 0 <= i < self.W**2:

                    neighbour = grid[i]
                    if neighbour.isCollapsed() == False:

                        new_options, changed = self.getNewOptions(neighbour.options,cell.options,dir)
                        if changed:

                            new_neighbour = Cell(nx,ny)


                            new_neighbour.options = new_options
                            grid[i] = new_neighbour
                            applyStack.append(new_neighbour)




    def getNewOptions(self, oldOptions, limitingCellOptions, direction):
        # old options are the options this cell used to have
        # limitingCellOptions are the options of the cell that is applying the rules to this cell
        # direction is the direction from the limiting cell to this cell, to get what rules apply
        res = []

        for option in limitingCellOptions:
            available = option.allowed[direction]
            new_options = WFC.intersection(oldOptions,available)
            res = WFC.union(res,new_options)

        changed = False
        for t in oldOptions:
            if t not in res:
                changed = True

        return res, changed


    def spawnWalk(self,grid,spawnx,spawny):

        spawnCell = grid[self.index(spawnx,spawny)]

        reachable = [spawnCell]
        for cell in reachable:

            x,y = cell.x,cell.y

            # UP
            if y > 0:
                neighbour = grid[self.index(x,y-1)]
                if cell.checkWalkingRules(0):

                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # DOWN
            if y < self.W-1:
                neighbour = grid[self.index(x,y+1)]
                if cell.checkWalkingRules(2):


                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # LEFT
            if x > 0:
                neighbour = grid[self.index(x-1,y)]
                if cell.checkWalkingRules(3):


                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # RIGHT
            if x < self.W-1:
                neighbour = grid[self.index(x+1,y)]
                if cell.checkWalkingRules(1):


                    if neighbour not in reachable:
                        reachable.append(neighbour)


        for cell in grid:

            if cell.isCollapsed() and not cell.getFinalOption().visit:
                continue

            if cell not in reachable: return False

        return True


    def drawGrid(self,grid,screen):

        pygame.event.pump() # gotta clear the event list every now and then...

        for i in range(self.W):
            for j in range(self.W):

                grid[self.index(i,j)].render(screen,i*self.SCL,j*self.SCL,self.SCL)

        pygame.display.update()

    def getLowestEntropy(self,grid): # get uncollapsed cells with lowest entropy
        s = sorted(grid, key=lambda c: len(c.options))

        uncollapsed = list(filter(lambda c: not c.isCollapsed(), s))

        if len(uncollapsed) == 0:
            return uncollapsed

        lowestEntropy = len(uncollapsed[0].options)
        lowest = filter(lambda c: len(c.options) == lowestEntropy, uncollapsed)

        return list(lowest)


    def index(self,x,y):
        return x+self.W*y

    @staticmethod
    def intersection(a,b): # intersection of 2 lists
        return [i for i in a if i in b]

    @staticmethod
    def union(a,b): # union of 2 lists
        return b + [i for i in a if i not in b]
