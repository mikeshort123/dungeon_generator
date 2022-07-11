import pygame,random

class Tile():

    def __init__(self, name, img, edge_rules,weight,walking_rules,visit):

        self.name = name
        self.img = img
        self.size = len(self.img)
        self.edge_rules = edge_rules
        self.weight = weight
        self.walking_rules = walking_rules
        self.visit = visit

    def rotate(self, name): # return a copy of the tile rotated 90 degrees clockwise
        new_img = [
            [self.img[self.size-i-1][j] for i in range(self.size)] for j in range(self.size)
        ]
        new_edges = [self.edge_rules[-1]] + self.edge_rules[:-1]
        new_walking = [self.walking_rules[-1]] + self.walking_rules[:-1]

        return Tile(name,new_img, new_edges, self.weight,new_walking,self.visit)


    def generateRules(self,tileList): # generate lists of tiles showing what tiles fit to this one

        self.allowed = {
            "UP" : [],
            "DOWN" : [],
            "LEFT" : [],
            "RIGHT" : []
        }

        self.walkable = {
            "UP" : [],
            "DOWN" : [],
            "LEFT" : [],
            "RIGHT" : []
        }

        for t in tileList:

            #UP
            if self.edge_rules[0] == t.edge_rules[2][::-1]:
                self.allowed["UP"].append(t)
                if self.walking_rules[0]: self.walkable["UP"].append(t)
            #DOWN
            if self.edge_rules[2] == t.edge_rules[0][::-1]:
                self.allowed["DOWN"].append(t)
                if self.walking_rules[2]: self.walkable["DOWN"].append(t)
            #LEFT
            if self.edge_rules[3] == t.edge_rules[1][::-1]:
                self.allowed["LEFT"].append(t)
                if self.walking_rules[3]: self.walkable["LEFT"].append(t)
            #RIGHT
            if self.edge_rules[1] == t.edge_rules[3][::-1]:
                self.allowed["RIGHT"].append(t)
                if self.walking_rules[1]: self.walkable["RIGHT"].append(t)
