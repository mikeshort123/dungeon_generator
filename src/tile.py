import pygame,random

class Tile():

    def __init__(self, img, edge_rules,weight,walking_rules,visit):

        self.img = img
        self.size = len(self.img)
        self.edge_rules = edge_rules
        self.weight = weight
        self.walking_rules = walking_rules
        self.visit = visit

    def rotate(self): # return a copy of the tile rotated 90 degrees clockwise
        new_img = [
            [self.img[self.size-i-1][j] for i in range(self.size)] for j in range(self.size)
        ]
        new_edges = [self.edge_rules[-1]] + self.edge_rules[:-1]
        new_walking = [self.walking_rules[-1]] + self.walking_rules[:-1]

        return Tile(new_img, new_edges, self.weight,new_walking,self.visit)


    def render(self,screen,x,y,size): # draw the tile from img
        pw = size // self.size

        for i in range(self.size):
            tx = x + i*pw
            for j in range(self.size):
                ty = y + j*pw

                c = self.img[j][i].colour

                pygame.draw.rect(screen,c,(tx,ty,pw,pw))


    def generateRules(self,tileList): # generate lists of tiles showing what tiles fit to this one

        self.allowed = {
            "UP" : [],
            "DOWN" : [],
            "LEFT" : [],
            "RIGHT" : []
        }

        for t in tileList:

            #UP
            if self.edge_rules[0] == t.edge_rules[2][::-1]:
                self.allowed["UP"].append(t)
            #DOWN
            if self.edge_rules[2] == t.edge_rules[0][::-1]:
                self.allowed["DOWN"].append(t)
            #LEFT
            if self.edge_rules[3] == t.edge_rules[1][::-1]:
                self.allowed["LEFT"].append(t)
            #RIGHT
            if self.edge_rules[1] == t.edge_rules[3][::-1]:
                self.allowed["RIGHT"].append(t)
