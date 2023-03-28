import random
import numpy as np
import pandas as  pd

class Player:
    def __init__(self, name, appearance, money=1500):
        self.name = name
        self.appearance = appearance
        self.money = money
        self.properties = []
        self.properties_value = sum(prpt.price for prpt in self.properties)
        self.position = 0
        self.jail = False
        self.jail_cards = 0
        self.jail_turns = 0
        self.doubles = 0
        self.doubles_rolls = 0
        
        def move(self, steps):
            self.position = (self.position + steps) % 40

        def buy_property(self, property):
            self.properties.append(property)
            self.money -= property.price

        def pay_rent(self, property):
            rent = property.rent
            if property.owner and property.owner != self:
                self.money -= rent
                property.owner.money += rent

        def is_bankrupt(self):
            return self.money < 0

class Property: # Cities and places
    def __init__(self, name, price, rent):
        self.name = name
        self.price = price
        self.rent = rent
        self.owner = None

    def upgrade(self, name, cur_price, cur_rent):
        self.price = 0.5 * cur_price
        self.rent = cur_rent * 1.5
class Chance:
    def __init__(self, name, action):
        self.name = name
        self.action = action   
