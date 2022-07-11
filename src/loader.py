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

        startx,starty = data["startx"],data["starty"]
        endx,endy = data["endx"],data["endy"]

        biomes = []
        for biomepath in data["biomes"]:
            biomes.append(Biome(biomepath))

        Loader.generateAllTileRules(biomes)

        distribution_settings = data["distribution"]
        distribution = [[biomes[distribution_settings["default"]] for j in range(height)] for i in range(width)]
        Loader.applyDistributionModifiers(distribution,distribution_settings["modifiers"],biomes)

        map = Map(width,height,startx,starty,endx,endy,distribution = distribution)

        for structure in data["structures"]:
            Loader.blitStructure(map,structure,biomes)

        if data["blank_edge"]:
            Loader.drawBlankEdges(map,distribution,width,height)

        return map


    @staticmethod
    def drawBlankEdges(map,distribution,width,height):
        for i in range(width):
            Loader.drawBlankPiece(map,distribution,i,0)
            Loader.drawBlankPiece(map,distribution,i,height-1)
        for j in range(height):
            Loader.drawBlankPiece(map,distribution,0,j)
            Loader.drawBlankPiece(map,distribution,width-1,j)


    @staticmethod
    def drawBlankPiece(map,distribution,x,y):
        if not map.getCell(x,y).isCollapsed():
            map.collapseCell(x,y,distribution[x][y].default)


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
        for i,row in enumerate(distribution):
            for j in range(len(row)):
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
