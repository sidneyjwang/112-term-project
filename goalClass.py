################################
# goal class
################################

class Goal:
    def __init__ (self, x, y):
        self.counter = 100
        self.x = x
        self.y = y
    def decreaseCounter(self):
        if self.counter > 0:
            self.counter -= 1