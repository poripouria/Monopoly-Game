import random
import numpy as np
import pandas as  pds

property_list = []
df = pd.read_excel("_Data/Properties-Detail.xlsx")
for place in df["place"]:
    property_list.append(place)
#print(property_list)

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
        # print("Dices roll: ", self.current_rolled1, self.current_rolled2)
        return self.current_rolled1, self.current_rolled2, self.rolled_sum

class Player:
    def __init__(self, name, appearance, money=1500):
        self.name = name
        self.appearance = appearance
        self.money = money
        self.properties = []
        self.properties_value = sum(prpt.price for prpt in self.properties)
        self.countries = []
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
            # TODO_: complete this
            """same_owner = True
            group_properties = [prpt for prpt in self.properties if prpt.country == property.country]
            for prpt in group_properties:
                if prpt.owner != property.owner:
                    same_owner = False
                    break
            if same_owner:
                for prpt in group_properties:
                    """

        def sell_property(self, property):
            self.properties.remove(property)
            self.money += 0.8 * property.price

        def pay_rent(self, property):
            rent = property.rent
            if property.owner and property.owner != self:
                self.money -= rent
                property.owner.money += rent

        def is_bankrupt(self):
            return self.money < 0

class Property:                                                     # Cities and places
    def __init__(self, name, type, country, price, rent):
        self.name = name
        self.country = country
        self.type = type
        self.price = price
        self.rent = rent
        self.owner = None

    def upgrade(self, name, type, country, cur_price, cur_rent):    # Build Hotels and Apartments
        if self.country in self.owner.countries:
            self.price = 0.5 * cur_price
            self.rent = cur_rent * 1.5

class Chance:
    def __init__(self, name, action):
        self.name = name
        self.action = action   
