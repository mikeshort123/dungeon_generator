

class Pixel:

    def __init__(self,name,colour):
        self.name = name
        self.colour = colour

    @staticmethod
    def process(data):
        pixels = []
        for p in data:
            pixels.append(Pixel(p["name"],p["colour"]))
        return pixels
