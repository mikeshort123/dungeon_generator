

class Pixel:

    def __init__(self,name,colour):
        self.name = name
        self.colour = colour

    @staticmethod
    def process(data,biome_name):
        pixels = []
        for p in data:
            pixels.append(Pixel(biome_name+"."+p["name"],p["colour"]))
        return pixels
