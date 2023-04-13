import random
import numpy as np
from copy import deepcopy

all_possible_actions = ["buy", "sell", "upgrade", "use_jail_card", "auction", "nothing_just_stay"]

class Player:
    def __init__(self, name, appearance=None, money=1500):
        self.name = name
        self.appearance = appearance
        self.money = money
        self.properties_value = 0
        self.wealth = money
        self.properties = []
        self.countries = []
        self.position = 0
        self.jail = False
        self.jail_turns = 0
        self.jail_cards = 0
        self.dices = [0, 0]
        self.doubles = False
        self.doubles_rolls = 0

    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]

        if properties[position].type in ["city" ,"service_centers"]:
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if input(f"Do you want to buy it (you have ${self.money})? (y/n) ") == "y":
                    self.buy_property(properties[position], properties)
                    if properties[position].owner == self:
                        print(f"{self.name} bought {properties[position].name}.")
                else:
                    print(f"{self.name} didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.money < 100:
                    print(f"ALARM: You have less than $100! Better to sell!")
                if input(f"Do you want to sell {properties[position].name} for {0.8 * properties[position].price}? (y/n) ") == "y":
                    self.sell_property(properties[position], properties)
                    print(f"{self.name} soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"{self.name} didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if input(f"Do you want to upgrade {properties[position].name} for {1.5 * properties[position].price}? (y/n) ") == "y":
                        current_price = properties[position].price
                        self.upgrade_property(properties[position])
                        if properties[position].is_upgrade:
                            print(f"{self.name} upgraded {properties[position].name} for {0.5*current_price}.\t(Upgraded {properties[position].upgrade_level} times)")
                    else:
                        print(f"{self.name} didn't upgrade {properties[position].name}.")
        if properties[position].type == "stay_place":
            if properties[position].name == "Go (Collect $200)":
                pass
            elif properties[position].name == "Jail":
                if self.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    if self.doubles:
                        self.doubles = False
                        self.doubles_rolls = 0
                    self.position = 9
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail.")
            elif properties[position].name == "Auction (Trade)":
                #TODO_: After compliting auction function, add it here
                prop_index = int(input("Inter Index of property you wanna treade (Inter -1 to pass): "))
                if prop_index == -1:
                    print(f"{self.name} prefer not to trade.")
                elif prop_index in self.properties.index:
                    pass
            elif properties[position].name == "Free Parking":
                print(f"Enjoy your free parking {self.name}!")
            elif properties[position].name == "Chance":
                self.chance(players)
            elif properties[position].name == "Income Tax":
                print(f"{self.name} paied ${0.1 * self.money} to the bank for Income Tax!")
                self.money -= 0.1 * self.money
                self.wealth = self.money + self.properties_value
            elif properties[position].name == "Luxury Tax":
                self.money -= 200
                print(f"{self.name} paied $200 to the bank for Luxury Tax!")
                self.wealth = self.money + self.properties_value
            elif properties[position].name == "Treasure":
                rand_mony = random.randint(5, 20)*10
                print(f"{self.name} got ${rand_mony} from the bank!")
                self.money += rand_mony
                self.wealth = self.money + self.properties_value
            else:
                raise Exception("Something went wrong in STAY_PLACE POSITIONS.")

    def roll_dices(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        roll_result = d1 + d2
        if d1 == d2:
            self.doubles_rolls += 1
            if self.doubles_rolls > 2:
                if self.jail_cards > 0 and input(f"You rolled double more than 3 times (Jail Rule). Do you want to use your Jail-Free card? (y/n) ") == "y":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    self.position = 9
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail becouse of 3 doubles rolls.")
                self.doubles = False
                self.doubles_rolls = 0
                return
            if self.jail:
                self.jail_turns -= 1
                if self.jail_turns == 0:
                    self.jail = False
                print(f"{self.name} is still in jail and couldn't roll again.")
                self.doubles = False
                self.doubles_rolls = 0
                return
            self.doubles = True
            print(f"{self.name} rolled double ({d1}, {d2}),next turn would be his/her again!")
        else:
            self.doubles = False
            self.doubles_rolls = 0
            print(f"{self.name} rolled {d1} and {d2}")
        self.dices[0] = d1
        self.dices[1] = d2
        self.move(roll_result)
        return d1, d2, roll_result
        
    def move(self, steps):
        if self.position + steps >= 40:
            self.money += 200
            self.wealth = self.money + self.properties_value
            print(f"{self.name} collected $200 from the bank for passing Go.")
            self.position = (self.position + steps) % 40
        else:
            self.position += steps
        self.wealth = self.money + self.properties_value
            
    def chance(self, players):
        commands = [
            "Go to Jail for 2 rounds",
            "Pay $50 to all players",
            "Give $50 from all players",
            "Get 1 Jail-Free card",
            "Roll the dice again",
            # f"Travel to {random.choice()}",
            "Nothing..."]
        command = random.choice(commands)
        print("Command is: " + command)
        if command == "Go to Jail for 2 rounds":
            if self.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                self.jail_cards -= 1
                self.position = 9
                self.jail = True
                self.jail_turns += 1
                print(f"{self.name} used a get out of jail free card (1 round left).")
            else:
                self.position = 9
                self.jail = True
                self.jail_turns += 2
                print(f"{self.name} went to jail for 2 rounds.")
        elif command == "Pay $50 to all players":
            for player in players:
                if player != self:
                    player.money += 50
                    self.money -= len(players) * 50 - 50
                    player.wealth = player.money + player.properties_value
            self.wealth = self.money + self.properties_value

        elif command == "Give $50 from all players":
            for player in players:
                if player != self:
                    player.money -= 50
                    self.money += 50
                    player.wealth = player.money + player.properties_value
            self.wealth = self.money + self.properties_value
        elif command == "Get 1 Jail-Free card":
            self.jail_cards += 1
        elif command == "Roll the dice again":
            self.doubles = True
        elif command == "Nothing...":
            pass
        else:
            raise Exception("Something went wrong with the CHANCE COMMAND.")

    def buy_property(self, property, properties):
        if property.price < self.money:
            property.buy(self, properties)
        else:
            print(f"{self.name} don't have enough money to buy it.") 

    def upgrade_property(self, property):      # Build Hotels and Apartments
        if property.upgrade_time < 3:
            if property.price < 2 * self.money:
                property.upgrade()
            else:
                print(f"{self.name} don't have enough money to Build here.")
        else:
            print(f"{property.name} couldn't UPGRADE anymore.")

    def sell_property(self, property):
        self.properties.remove(property)
        self.properties_value -= property.price
        self.money += property.sell_ratio * property.price
        property.owner = None
        if property.country in self.countries:
            self.countries.remove(property.country)
        self.wealth = self.money + self.properties_value

    def auction(self, property1, property2):
        pass

    def pay_rent(self, property):
        rent = property.rent
        if property.owner and property.owner != self:
            self.money -= rent
            property.owner.money += rent
        self.wealth = self.money + self.properties_value

    def is_bankrupt(self):
        return self.money < 0

    def print_player_status(self, on_property):
        print(f"| _____________{self.name}_____________")
        print(f"| {self.name} has {self.doubles_rolls} doubles rolls")
        print(f"| {self.name} has ${self.wealth} wealth")
        print(f"| {self.name} has ${self.money} money left")
        print(f"| {self.name} has ${self.properties_value} properties value")
        print(f"| {self.name} has {self.properties} properties")
        print(f"| {self.name} has {self.countries} countries")
        print(f"| {self.name} is on {self.position} position ({on_property[self.position].name})")
        print(f"| {self.name} is {'in' if self.jail else 'not in'} jail")
        print(f"| {self.name} has {self.jail_turns} jail turns")
        print(f"| {self.name} has {self.jail_cards} jail cards")
        print(f"| {self.name} is {'bankrupt' if self.is_bankrupt() else 'not bankrupt'}")

    def __str__(self):
        return ("\n" + "TYPE: " + str(type(self).__name__) + 
                "\n" + "Name: " + str(self.name) + 
                "\n" + "Money: " + str(self.money) + 
                "\n" + "Wealth: " + str(self.wealth) + 
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
    def __init__(self, name, depth=3, appearance=None, money=1500):
        super().__init__(name, appearance, money)
        self.depth = depth

    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]

        if properties[position].type == "city" or properties[position].type == "service_centers":
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if self.make_decision(state) == "buy":
                    self.buy_property(properties[position], properties)
                    print(f"{self.name} bought {properties[position].name}.")
                else:
                    print(f"{self.name} didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.make_decision(state) == "sell":
                    self.sell_properties[position](properties[position])
                    print(f"{self.name} soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"{self.name} didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if self.make_decision(state) == "upgrade":
                        print(f"{self.name} upgraded {properties[position].name} for {0.5*properties[position].price}.")
                        self.upgrade_property(properties[position])
                    else:
                        print(f"{self.name} didn't upgrade {properties[position].name}.")
        if properties[position].type == "stay_place":
            if properties[position].name == "Go (Collect $200)":
                pass
            elif properties[position].name == "Jail":
                if self.jail_cards > 0 and self.make_decision(state) == "use_jail_card":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    if self.doubles:
                        self.doubles = False
                        self.doubles_rolls = 0
                    self.position = 9
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail.")
            elif properties[position].name == "Auction (Trade)":
                #TODO_: After compliting auction function, add it here
                print("Currently Auction (Trade) is not available!")
                pass
            elif properties[position].name == "Free Parking":
                print(f"Enjoy your free parking {self.name}!")
            elif properties[position].name == "Chance":
                self.chance(players)
            elif properties[position].name == "Income Tax":
                print(f"{self.name} paied ${0.1 * self.money} to the bank for Income Tax!")
                self.money -= 0.1 * self.money
            elif properties[position].name == "Luxury Tax":
                self.money -= 200
                print(f"{self.name} paied $200 to the bank for Luxury Tax!")
            elif properties[position].name == "Treasure":
                rand_mony = random.randint(5, 20)*10
                print(f"{self.name} got ${rand_mony} from the bank!")
                self.money += rand_mony
            else:
                raise Exception("Something went wrong in STAY_PLACE POSITIONS.")

    def current_possible_actions(self, state):
        possible_actions = []
        properties = state["properties"]
        if properties[self.position].type == "city" or properties[self.position].type == "service_centers":
            if properties[self.position].owner == None:
                possible_actions.append(all_possible_actions[0]) # "buy"
                possible_actions.append(all_possible_actions[5]) # "nothing_just_stay"
            elif properties[self.position].owner == self:
                possible_actions.append(all_possible_actions[1]) # "sell"
                possible_actions.append(all_possible_actions[5]) # "nothing_just_stay"
                if (properties[self.position].type == "city" and properties[self.position].country in self.countries) or (properties[self.position].type == "service_centers" and "Service-Centers" in self.countries):
                    possible_actions.append(all_possible_actions[2]) # "upgrade"
        if properties[self.position].type == "stay_place":
            if properties[self.position].name == "Jail":
                possible_actions.append(all_possible_actions[3]) # "use_jail_card"
                possible_actions.append(all_possible_actions[5]) # "nothing_just_stay"
            elif properties[self.position].name == "Auction (Trade)":
                possible_actions.append(all_possible_actions[4]) # "auction"
                possible_actions.append(all_possible_actions[5]) # "nothing_just_stay"
        return possible_actions

    def make_decision(self, state):
        actions = self.current_possible_actions(state)
        
        action_values = []
        for action in actions:
            new_state = self.get_next_state(state, action=action)
            value = self.expectiminimax(new_state, self.depth)
            action_values.append((action, value))
            
        sorted_actions = sorted(action_values, key=lambda x: x[1], reverse=True)
        best_action = sorted_actions[0][0]

        return best_action

    def expectiminimax(self, state, depth):
        if state["rounds_left"] == 0 or depth == 0:
            return self.evaluate_state(state)

        # check if it's the AI Agent's turn
        if state["current_player"] == self:
            # maximize the expected value
            max_value = -np.inf
            actions = self.current_possible_actions(state)
            for action in actions:
                new_state = self.get_next_state(state, action=action)
                value = self.expectiminimax(new_state, depth-1)
                max_value = max(max_value, value)
            return max_value
        # check if it's the Minimum player's turn
        elif state["current_player"] != self:
            # minimize the expected value
            min_value = np.inf
            actions = self.current_possible_actions(state)
            for action in actions:
                new_state = self.get_next_state(state, action=action)
                value = self.expectiminimax(new_state, depth-1)
                min_value = min(min_value, value)
            return min_value
        # otherwise, it's the chance player's turn
        else:
            # calculate the expected value
            total_value = 0
            probabilities = all_rolls()
            for outcome, probability in probabilities.items():
                new_state = self.get_next_state(state, outcome=outcome)
                value = self.expectiminimax(new_state, depth-1)
                total_value += value * probability
            return total_value

    def evaluate_state(self, state):
        value = 10
        return value

    def get_next_state(self, state, action=None, outcome=None):
        new_state = deepcopy(state)
        current_player = new_state["current_player"]
        properties = new_state["properties"]
        if action != None:
            if action == "buy":
                current_player.buy_property(properties[current_player.position], properties)
            elif action == "sell":
                current_player.sell_property(properties[current_player.position])
            elif action == "upgrade":
                current_player.upgrade_property(properties[current_player.position])
            elif action == "use_jail_card":
                current_player.jail_cards -= 1
                current_player.jail = False
            elif action == "auction":
                #TODO_: After compliting auction function, add it here
                pass
            elif action == "nothing_just_stay":
                pass
            else:
                raise Exception("Something went wrong in get_next_state function.")
        if outcome != None:
            current_player.move(int(outcome))
        # Give turn to next player
        new_state["current_player"] = new_state["players"][((new_state["turn_counter"]+1) % new_state["players_num"])]

        return new_state

def all_rolls():
    all_results = []

    for i in range(2,13):
        favorable = 0
        for j in range(1,7):
            if i-j >= 1 and i-j <= 6:
                favorable += 1
        probability = favorable / 36
        all_results.append((i,probability))
    """
        2 : (1+1)                                           = 1/36
        3 : (2+1) & (1+2)                                   = 1/18
        4 : (2+2) & (3+1) & (1+3)                           = 1/12
        5 : (2+3) & (3+2) & (4+1) & (1+4)                   = 1/9
        6 : (1+5) & (2+4) & (3+3) & (4+2) & (5+1)           = 5/36
        7 : (1+6) & (2+5) & (3+4) & (4+3) & (5+2) & (6+1)   = 1/6
        ...
        11: (5+6) & (6+5)                                   = 1/18  
        12: (6+6)                                           = 1/36
    """
    return all_results
