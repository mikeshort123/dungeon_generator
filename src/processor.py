import json

class Processor:

    class Rule:

        def __init__(self,data):
            self.target = data["target"]
            self.img = data["match"]

        def match(self,grid,x,y):

            for i,row in enumerate(self.img):
                for j,v in enumerate(row):
                    if v == None: continue
                    dx,dy = x+i-1, y+j-1
                    if not (0 <= dx < len(grid) and 0 <= dy < len(grid[0])): return False

                    if grid[dx][dy] != v: return False
            return True

    def __init__(self,map,fn):

        f = open(fn,"r")
        data = json.load(f)
        f.close()

        pixel_grid = map.getPixelGrid()
        self.grid = [[data["encoder"][v.name] for v in row] for row in pixel_grid]

        self.rules = [Processor.Rule(d) for d in data["rules"]]


    def applyRules(self):
        new_grid = [[self.applyRulesToPoint(i,j) for i in range(len(self.grid))] for j in range(len(self.grid[0]))]
        self.grid = new_grid

    def applyRulesToPoint(self,x,y):

        for rule in self.rules[::-1]:
            if rule.match(self.grid,x,y):
                return rule.target
        return self.grid[x][y]



    def save(self,fn):
        s = "" # turn grid to string
        for row in self.grid:
            for v in row:
                s += str(v) + ","
            s += "\n"

        f = open(fn,"w+") # save grid to file
        f.write(s)
        f.close()
