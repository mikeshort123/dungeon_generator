

class Processor:

    def __init__(self,map,encoder):

        pixel_grid = map.getPixelGrid()
        self.grid = [[encoder[v.name] for v in row] for row in pixel_grid]


    def save(self,fn):
        s = "" # turn grid to string
        for row in self.grid:
            for v in row:
                s += str(v) + ","
            s += "\n"

        f = open(fn,"w+") # save grid to file
        f.write(s)
        f.close()
