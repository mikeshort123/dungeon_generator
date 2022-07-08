import json
from src.tile import Tile

class Biome:

    biomes = []

    def __init__(self,fn):

        Biome.biomes.append(self) # add new biome to global list of biomes

        f = open(fn,"r") # load biome data from file
        data = json.load(f)
        f.close

        self.name = data["name"]
        self.tileList = {}
        for tile in data["tiles"]:
            self.loadTile(tile)


    def loadTile(self,data): # load tile from json format

        name = data["name"]
        img = data["img"]
        edge_rules = data["edge_rules"]
        rotations = data["rotations"]
        weight = data["weight"]
        walking_rules = data["walking_rules"]
        visit = data["visit"]

        t = Tile(img,edge_rules,weight,walking_rules,visit)

        self.tileList[name] = t

        if rotations == 4: # some tiles need to be rotated
            for i in range(3):
                new_name = name + "_" + str(i+2)
                t = t.rotate()
                self.tileList[new_name] = t


    @staticmethod
    def getAllTiles():
        tiles = []
        for biome in Biome.biomes:
            tiles += biome.tileList.values()
        return tiles

    @staticmethod
    def generateAllTileRules():
        tiles = Biome.getAllTiles()
        for t in tiles:
            t.generateRules(tiles)
