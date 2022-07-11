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


    def render(self,screen,x,y,size):

        if self.isCollapsed():
            self.getFinalOption().render(screen,x,y,size)

        else:
            c = 100
            pygame.draw.rect(screen,(c,c,c),(x,y,size,size))
