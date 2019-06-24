class Node:
    def __init__(self, x=0, y=0, time=0):
        self.x = x
        self.y = y
        self.t = time

        self.hCost = 0
        self.gCost = 0
        self.fCost = self.getfCost()

        self.parentNode = None

        self.openbyStart = False
        self.openbyEnd = False

        # 1 = N, 2 = S, 3 = W, 4 = E
        self.direction = 0

    def getfCost(self):
        return self.hCost + self.gCost

    def equals(self, p1):
        if (p1.x == self.x and p1.y == self.y and p1.t == self.t):
            return True
        return False
