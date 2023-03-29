import random

class DoubleDice():
    def __init__(self, sides=6):
        self.sides = sides
        self.current_rolled1 = 0
        self.current_rolled2 = 0
        self.rolled_sum = 0

    def roll_double_dice(self):
        self.current_rolled1 = random.randint(1, self.sides)
        self.current_rolled2 = random.randint(1, self.sides)
        self.rolled_sum = self.current_rolled1 + self.current_rolled2
        return self.current_rolled1, self.current_rolled2, self.rolled_sum


