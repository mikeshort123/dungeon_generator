import pygame

from src.tile import Tile


class Cell():

    def __init__(self,x,y):

        self.x = x
        self.y = y

        self.options = Tile.tileList.values()

    def collapse(self,option):
        self.options = [option]
        return self

    def isCollapsed(self):
        return len(self.options) == 1

    def getFinalOption(self):
        return self.options[0]

    def checkWalkingRules(self,i):
        f = False
        for option in self.options:
            f = f or option.walking_rules[i]
        return f

    def render(self,screen,x,y,size):

        if self.isCollapsed():
            self.getFinalOption().render(screen,x,y,size)

        else:
            c = 100
            pygame.draw.rect(screen,(c,c,c),(x,y,size,size))
