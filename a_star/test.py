import operator


class Lol:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"{self.a} {self.b}"


lol = [Lol(1, 20), Lol(3, 10), Lol(-1, 12), Lol(-20, 8), Lol(6, 11)]
lol.sort(key=operator.attrgetter("b"))
