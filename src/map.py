from src.cell import Cell

class Map:

    def __init__(self,W,distribution=None):

        self.W = W

        self.grid = []
        for j in range(self.W):
            for i in range(self.W):
                biome = None
                if distribution:
                    biome = distribution[i][j]
                self.grid.append(Cell(i,j,biome=biome))

        self.updateList = []


    def collapseCell(self,x,y,tile): # collapse cell by setting its options to one tile
        self.updateCell(x,y,[tile])


    def updateCell(self,x,y,tiles):
        cell = Cell(x,y) # make a new cell rather than modifying old ones as to not change cells in previous steps stored for backtracking
        self.setCell(x,y,cell)
        cell.options = tiles
        self.updateList.append(cell)


    def getCell(self,x,y):
        return self.grid[self.index(x,y)]

    def setCell(self,x,y,cell):
        self.grid[self.index(x,y)] = cell

    def index(self,x,y):
        return x+self.W*y

    def copy(self):
        new_map = Map(self.W)
        new_map.grid = self.grid[:]
        return new_map

    def drawImage(self,img,biome,x,y):

        for j, row in enumerate(img):
            for i, v in enumerate(row):
                self.collapseCell(x+i,y+j,biome.tileList[v])
