import pygame

from src.tile import Tile


class Cell():

    def __init__(self,x,y,biome=None):

        self.x = x
        self.y = y

        if biome:
            self.options = list(biome.tileList.values())
        else:
            self.options = []

    def isCollapsed(self):
        return len(self.options) == 1

    def getFinalOption(self):
        return self.options[0]
