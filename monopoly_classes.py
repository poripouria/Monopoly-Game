import random

class Player:
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
        self.properties = []
        self.position = 0
        self.jail = False
        self.jail_cards = 0
        self.jail_turns = 0
        self.doubles = 0
        self.doubles_rolls = 0
        