from src.cell import Cell

class Map:

    def __init__(self,W,startx,starty,endx,endy,distribution=None):

        self.W = W

        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy

        self.grid = []
        if distribution:
            for j in range(self.W):
                for i in range(self.W):
                    self.grid.append(Cell(i,j,biome=distribution[i][j]))

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
        new_map = Map(self.W,self.startx,self.starty,self.endx,self.endy)
        new_map.grid = self.grid[:]
        return new_map

    def drawImage(self,img,biome,x,y):
        for j, row in enumerate(img):
            for i, v in enumerate(row):
                self.collapseCell(x+i,y+j,biome.tileList[v])


    def getPixelGrid(self):

        img_size = self.grid[0].getFinalOption().size
        pixel_grid = [[self.getCell(i//img_size,j//img_size).getFinalOption().img[j%img_size][i%img_size] for i in range(self.W*img_size)] for j in range(self.W*img_size)]
        return pixel_grid
