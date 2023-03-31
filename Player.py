import random
import numpy as np

class Player:
    def __init__(self, name, appearance=None, money=1500):
        self.name = name
        self.appearance = appearance
        self.money = money
        self.properties = []
        self.properties_value = 0
        self.countries = []
        self.position = 0
        self.jail = False
        self.jail_turns = 0
        self.jail_cards = 0
        self.doubles = False
        self.doubles_rolls = 0
        
    def roll_dices(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        roll_result = d1 + d2
        if d1 == d2:
            if self.jail:
                self.jail_turns -= 1
                if self.jail_turns == 0:
                    self.jail = False
                print(f"{self.name} is still in jail and couldn't roll again.")
                pass
            if self.doubles_rolls > 2:
                if self.jail_cards > 0 and input(f"You rolled double more than 3 times (Jail Rule). Do you want to use your Jail-Free card? (y/n) ") == "y":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    self.position = 10
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail becouse of 3 doubles rolls.")
                pass
            self.doubles = True
            self.doubles_rolls += 1
            print(f"{self.name} rolled double ({d1}, {d2}),next turn would be his/her again!")
        else:
            self.doubles = False
            self.doubles_rolls = 0
            print(f"{self.name} rolled {d1} and {d2}")
        self.move(roll_result)
        return d1, d2, roll_result
        
    def move(self, steps):
        if self.position + steps >= 40:
            self.money += 200
            print(f"{self.name} collected $200 from the bank for passing Go.")
            self.position = (self.position + steps) % 40
        else:
            self.position += steps
            
    def chance(self, players):
        commands = [
            "Go to Jail for 2 rounds",
            "Pay $50 to all players",
            "Give $20 from all players",
            "Get 1 Jail-Free card",
            "Roll the dice again",
            "Nothing..."]
        command = random.choice(commands)
        print("Command is: " + command)
        if command == "Go to Jail for 2 rounds":
            if self.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                self.jail_cards -= 1
                self.position = 10
                self.jail = True
                self.jail_turns += 1
                print(f"{self.name} used a get out of jail free card (1 round left).")
            else:
                self.position = 10
                self.jail = True
                self.jail_turns += 2
                print(f"{self.name} went to jail for 2 rounds.")
        elif command == "Pay $50 to all players":
            for player in players:
                if player != self:
                    player.money += 50
                    self.money -= len(players) * 50 - 50
        elif command == "Give $20 from all players":
            for player in players:
                if player != self:
                    player.money -= 20
                    self.money += 20
        elif command == "Get 1 Jail-Free card":
            self.jail_cards += 1
        elif command == "Roll the dice again":
            self.doubles = True
        elif command == "Nothing...":
            pass
        else:
            raise Exception("Something went wrong with the CHANCE COMMAND.")

    def buy_property(self, property):
        if property.owner != self:
            self.properties.append(property)
            self.properties_value += property.price
            self.money -= property.price
            property.owner = self
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
        self.properties_value -= property.price
        self.money += 0.8 * property.price
        property.owner = None
        if property.country in self.countries:
            self.countries.remove(property.country)

    def pay_rent(self, property):
        rent = property.rent
        if property.owner and property.owner != self:
            self.money -= rent
            property.owner.money += rent

    def is_bankrupt(self):
        return self.money < 0

    def print_player_status(self):
        print(f"| _____________{self.name}_____________")
        print(f"| {self.name} has {self.doubles_rolls} doubles rolls")
        print(f"| {self.name} has ${self.money} money left")
        print(f"| {self.name} has {self.properties} properties")
        print(f"| {self.name} has ${self.properties_value} properties value")
        print(f"| {self.name} has {self.countries} countries")
        print(f"| {self.name} is on {self.position} position")
        print(f"| {self.name} is {'in' if self.jail else 'not in'} jail")
        print(f"| {self.name} has {self.jail_turns} jail turns")
        print(f"| {self.name} has {self.jail_cards} jail cards")
        print(f"| {self.name} is {'bankrupt' if self.is_bankrupt() else 'not bankrupt'}")

    def __str__(self):
        return ("\n" + "TYPE: " + str(type(self).__name__) + 
                "\n" + "Name: " + str(self.name) + 
                "\n" + "Money: " + str(self.money) + 
                "\n" + "Properties: " + str(self.properties) + 
                "\n" + "Countries: " + str(self.countries) + 
                "\n" + "Position: " + str(self.position) + 
                "\n" + "Jail: " + str(self.jail) + 
                "\n" + "Jail Cards: " + str(self.jail_cards) + 
                "\n" + "Jail Turns: " + str(self.jail_turns) + 
                "\n")

    def __repr__(self):
        return (str(self.name))

class AI_Agent(Player):
    def __init__(self, name, depth=5, appearance=None, money=1500):
        super().__init__(name, appearance, money)
        self.depth = depth

    def actions(self, dice1, dice2):
        return ["", "", ""]
        
    def expectiminimax(self, dice1, dice2):
        if self.depth == 0:
            pass
            
    def evaluate(self):
        pass
    
    def play(self, dice1, dice2):
        best_value = -np.inf
        best_action = None
        for action in self.actions(dice1, dice2):
            pass
        return best_action
