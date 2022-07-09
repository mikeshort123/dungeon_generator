import pygame, random
from src.cell import Cell
from src.tile import Tile
from src.map import Map

class WFC:

    def __init__(self,W,spawnx,spawny,drawFunction):

        self.spawnx = spawnx
        self.spawny = spawny

        self.W = W

        self.drawFunction = drawFunction

    def forceCollapse(self,updateList,map,x,y,tile):

        cell = map.getCell(x,y)
        cell.collapse(tile)
        if cell not in updateList: updateList.append(cell)


    def step(self,map):

        lowest = self.getLowestEntropy(map.grid)

        if len(lowest) == 0: # no more un-collapsed cells, grid is done, return true
            return map

        cell = random.choice(lowest)
        x, y = cell.x, cell.y

        if len(cell.options) == 0: # if no available picks, backtrack
            return None

        options = cell.options.copy()
        random.shuffle(options)
        for option in options: # try out each option (in a random order)

            next_map = map.copy()

            next_map.collapseCell(x,y,option)
            self.applyAllRules(next_map)

            if self.spawnWalk(next_map,self.spawnx,self.spawny):

                self.drawFunction(next_map)

                p_grid = self.step(next_map)
                if p_grid:
                    return p_grid

        return None


    def applyAllRules(self,map):

        while len(map.updateList) > 0:
            cell = map.updateList.pop()
        #for cell in map.updateList:


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

                if 0 <= nx < self.W and 0 <= ny < self.W:

                    neighbour = map.getCell(nx,ny)
                    if neighbour.isCollapsed() == False:

                        new_options, changed = self.getNewOptions(neighbour.options,cell.options,dir)
                        if changed:

                            new_neighbour = Cell(nx,ny)


                            new_neighbour.options = new_options
                            map.setCell(nx,ny,new_neighbour)
                            map.updateList.append(new_neighbour)




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


    def spawnWalk(self,map,spawnx,spawny):

        spawnCell = map.getCell(spawnx,spawny)

        reachable = [spawnCell]
        for cell in reachable:

            x,y = cell.x,cell.y

            # UP
            if y > 0:
                neighbour = map.getCell(x,y-1)
                if cell.checkWalkingRules(0):

                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # DOWN
            if y < self.W-1:
                neighbour = map.getCell(x,y+1)
                if cell.checkWalkingRules(2):


                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # LEFT
            if x > 0:
                neighbour = map.getCell(x-1,y)
                if cell.checkWalkingRules(3):


                    if neighbour not in reachable:
                        reachable.append(neighbour)

            # RIGHT
            if x < self.W-1:
                neighbour = map.getCell(x+1,y)
                if cell.checkWalkingRules(1):


                    if neighbour not in reachable:
                        reachable.append(neighbour)


        for cell in map.grid:

            if cell.isCollapsed() and not cell.getFinalOption().visit:
                continue

            if cell not in reachable: return False

        return True




    def getLowestEntropy(self,grid): # get uncollapsed cells with lowest entropy
        s = sorted(grid, key=lambda c: len(c.options))

        uncollapsed = list(filter(lambda c: not c.isCollapsed(), s))

        if len(uncollapsed) == 0:
            return uncollapsed

        lowestEntropy = len(uncollapsed[0].options)
        lowest = filter(lambda c: len(c.options) == lowestEntropy, uncollapsed)

        return list(lowest)


    @staticmethod
    def intersection(a,b): # intersection of 2 lists
        return [i for i in a if i in b]

    @staticmethod
    def union(a,b): # union of 2 lists
        return b + [i for i in a if i not in b]
