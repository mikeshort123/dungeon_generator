import json
from src.tile import Tile
from src.pixel import Pixel

class Biome:

    biomes = []

    def __init__(self,fn):

        Biome.biomes.append(self) # add new biome to global list of biomes

        f = open(fn,"r") # load biome data from file
        data = json.load(f)
        f.close()

        self.name = data["name"]

        self.pixels = Pixel.process(data["pixels"],self.name)

        self.tileList = {}
        for tile in data["tiles"]:
            self.loadTile(tile)

        self.default = None
        if data["default"]:
            self.default = self.tileList[data["default"]]


    def loadTile(self,data): # load tile from json format

        name = data["name"]
        img = data["img"]
        edge_rules = data["edge_rules"]
        rotations = data["rotations"]
        weight = data["weight"]
        walking_rules = data["walking_rules"]
        visit = data["visit"]

        t_img = [
            [self.pixels[v] for v in row] for row in img
        ]

        t = Tile(self.name+"."+name,t_img,edge_rules,weight,walking_rules,visit)

        self.tileList[name] = t

        if rotations == 4: # some tiles need to be rotated
            for i in range(3):
                new_name = name + "_" + str(i+2)
                t = t.rotate(self.name+"."+new_name)
                self.tileList[new_name] = t
