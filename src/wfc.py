import pygame, random
from src.cell import Cell
from src.tile import Tile
from src.map import Map

class WFC:

    dirList = [ # directions and offsets, used for looping through different connections
        ["UP",    0,-1],
        ["RIGHT", 1, 0],
        ["DOWN",  0, 1],
        ["LEFT", -1, 0]
    ]

    def __init__(self,W,spawnx,spawny,drawFunction=None):

        self.spawnx = spawnx
        self.spawny = spawny

        self.W = W

        self.drawFunction = drawFunction


    def step(self,map):

        lowest = self.getLowestEntropy(map.grid)

        if len(lowest) == 0: # no more un-collapsed cells, grid is done, return
            return map

        cell = random.choice(lowest)
        x, y = cell.x, cell.y

        if len(cell.options) == 0: # if no available picks, backtrack
            return None

        options = cell.options.copy()
        while option := self.getWeightedOption(options):


            next_map = map.copy()

            next_map.collapseCell(x,y,option)
            self.applyAllRules(next_map)

            if self.spawnWalk(next_map):

                if self.drawFunction: self.drawFunction(next_map)

                p_grid = self.step(next_map)
                if p_grid:
                    return p_grid

        return None


    def getWeightedOption(self,tiles): # used for pulling random items(weighted) from options of tiles
        if len(tiles) == 0:
            return False

        weights = [tile.weight for tile in tiles]
        cum_weights = [sum(weights[:i+1]) for i in range(len(weights))]

        r = random.random() * cum_weights[-1]
        f = filter(lambda w: w < r, cum_weights)
        index = sum(1 for _ in f)


        return tiles.pop(index)


    def applyAllRules(self,map):

        while len(map.updateList) > 0:
            cell = map.updateList.pop()

            x = cell.x
            y = cell.y

            for dir,dx,dy in WFC.dirList:
                nx,ny = x+dx, y+dy

                if not (0 <= nx < self.W and 0 <= ny < self.W): # if checking outside grid, skip to next direction
                    continue

                neighbour = map.getCell(nx,ny)
                if neighbour.isCollapsed(): # no point updating collapsed cells
                    continue

                new_options, changed = self.getNewOptions(neighbour.options,cell.options,dir)
                if changed:

                    map.updateCell(nx,ny,new_options)


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


    def spawnWalk(self,map):

        spawnCell = map.getCell(self.spawnx,self.spawny)

        reachable = [spawnCell]

        for cell in reachable:

            x,y = cell.x,cell.y

            for dir,dx,dy in WFC.dirList:
                nx,ny = x+dx, y+dy

                if not (0 <= nx < self.W and 0 <= ny < self.W): # if checking outside grid, skip to next direction
                    continue

                neighbour = map.getCell(nx,ny)
                if self.checkWalkable(neighbour,cell,dir):
                    if neighbour not in reachable:
                        reachable.append(neighbour)


        for cell in map.grid:
            if True in [o.visit for o in cell.options]:
                if cell not in reachable:
                    return False

        return True


    def checkWalkable(self,neighbour,cell,dir):

        for option in cell.options:
            for tile in option.walkable[dir]:
                if tile in neighbour.options:
                    return True

        return False




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
