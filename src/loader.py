import json

from src.biome import Biome
from src.map import Map

class Loader:

    @staticmethod
    def  loadWorld(fn):

        f = open(fn,"r")
        data = json.load(f)
        f.close()

        width = data["width"]
        height = data["height"]

        biomes = []
        for biomepath in data["biomes"]:
            biomes.append(Biome(biomepath))

        Loader.generateAllTileRules(biomes)

        distribution_settings = data["distribution"]
        distribution = [[biomes[distribution_settings["default"]] for i in range(width)] for j in range(height)]
        Loader.applyDistributionModifiers(distribution,distribution_settings["modifiers"],biomes)

        map = Map(width,distribution)

        for structure in data["structures"]:
            Loader.blitStructure(map,structure,biomes)

        if data["blank_edge"]:
            for i in range(width):
                if not map.getCell(i,0).isCollapsed(): map.collapseCell(i,0,distribution[i][0].default)
                if not map.getCell(i,width-1).isCollapsed(): map.collapseCell(i,width-1,distribution[i][width-1].default)
                if not map.getCell(0,i).isCollapsed(): map.collapseCell(0,i,distribution[0][i].default)
                if not map.getCell(width-1,i).isCollapsed(): map.collapseCell(width-1,i,distribution[width-1][i].default)

        return map


    @staticmethod
    def blitStructure(map,structure,biomes):
        map.drawImage(structure["image"],biomes[structure["biome"]],structure["xpos"],structure["ypos"])


    @staticmethod
    def applyDistributionModifiers(distribution,modifiers,biomes):
        for modifier in modifiers:

            if modifier["type"] == "circle":
                Loader.applyCircle(distribution,biomes[modifier["result"]],modifier["xpos"],modifier["ypos"],modifier["radius"])




    @staticmethod
    def applyCircle(distribution,result,x,y,r):
        for j,row in enumerate(distribution):
            for i in range(len(row)):
                if (i-x)**2 + (j-y)**2 < r**2:
                    distribution[i][j] = result


    @staticmethod
    def getAllTiles(biomes):
        tiles = []
        for biome in biomes:
            tiles += biome.tileList.values()
        return tiles

    @staticmethod
    def generateAllTileRules(biomes):
        tiles = Loader.getAllTiles(biomes)
        for t in tiles:
            t.generateRules(tiles)
