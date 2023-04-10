import copy
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
        self.dices = [0, 0]
        self.doubles = False
        self.doubles_rolls = 0
        self.all_pussible_actions = ["buy", "sell", "use_jail_card", "trade", "nothing_just_stay"]


    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]
        max_money = state["max_money"]
        max_rounds = state["max_rounds"]
        if properties[position].type in ["city" ,"service_centers"]:
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if input(f"Do you want to buy it (you have ${self.money})? (y/n) ") == "y":
                    self.buy_property(properties[position], properties)
                    print(f"You bought {properties[position].name}.")
                else:
                    print(f"You didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.money < 100:
                    print(f"ALARM: You have less than $100! Better to sell!")
                if input(f"Do you want to sell {properties[position].name} for {0.8 * properties[position].price}? (y/n) ") == "y":
                    self.sell_property(properties[position], properties)
                    print(f"You soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"You didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if input(f"Do you want to upgrade {properties[position].name} for {1.5 * properties[position].price}? (y/n) ") == "y":
                        print(f"You upgraded {properties[position].name} for {0.5*properties[position].price}.")
                        self.upgrade_property(properties[position])
                    else:
                        print(f"You didn't upgrade {properties[position].name}.")
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
                print("Currently Auction (Trade) is not available!")
                pass
            elif properties[position].name == "Free Parking":
                print("Enjoy your free parking!")
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

    def buy_property(self, property, properties):
        if property.price < self.money:
            self.properties.append(property)
            self.properties_value += property.price
            self.money -= property.price
            property.owner = self
            if property.type == "city":
                for i in range(40):
                    if properties[i].type == "city" and properties[i].country == property.country:
                        if properties[i].owner != self or properties[i].owner is None:
                            break
                else:
                    self.countries.append(property.country)
                    print(f"{self.name} got all the cities in {property.country}!")
            elif property.type == "service_centers":
                for i in range(40):
                    if properties[i].type == "service_centers":
                        if properties[i].owner != self or properties[i].owner is None:
                            break
                else:
                    self.countries.append("Service-Centers")
                    print(f"{self.name} got all the service centers!")
        else:
            print("You don't have enough money to buy it.") 

    def upgrade_property(self, property):      # Build Hotels and Apartments
        if property.upgrade_time <= 3:
            if property.price < 2 * self.money:
                property.upgrade()   
            else:
                print("You don't have enough money to Build here.")
        else:
            print(f"{property.name} couldn't UPGRADE anymore.")

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

    def print_player_status(self, on_property):
        print(f"| _____________{self.name}_____________")
        print(f"| {self.name} has {self.doubles_rolls} doubles rolls")
        print(f"| {self.name} has ${self.money} money left")
        print(f"| {self.name} has {self.properties} properties")
        print(f"| {self.name} has ${self.properties_value} properties value")
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

    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]
        rounds_left = state["rounds_left"]
        max_money = state["max_money"]
        if properties[position].type == "city" or properties[position].type == "service_centers":
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if self.make_decision(state) == "buy":
                    self.buy_property(properties[position], properties)
                    print(f"You bought {properties[position].name}.")
                else:
                    print(f"You didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.make_decision(state) == "sell":
                    self.sell_properties[position](properties[position])
                    print(f"You soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"You didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if self.make_decision(state) == "upgrade":
                        print(f"You upgraded {properties[position].name} for {0.5*properties[position].price}.")
                        self.upgrade_property(properties[position])
                    else:
                        print(f"You didn't upgrade {properties[position].name}.")
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
                print("Enjoy your free parking!")
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
        # get the current player's position and properties
        position = state.get_player_position(self)
        properties = state.get_player_properties(self)
        
        # define function to check if property can be bought
        def can_buy_property(property):
            return property.owner is None

        # define function to check if property can be sold
        def can_sell_property(property):
            return property.owner == self

        # define possible actions
        possible_actions = []

        # add actions to buy properties
        for property in state.board:
            if property.type in ["city", "service_centers"] and can_buy_property(property):
                possible_actions.append(("buy", property))

        # add actions to sell properties
        for property in properties:
            if can_sell_property(property):
                possible_actions.append(("sell", property))
        
        # add action to stay (do nothing)
        possible_actions.append(("stay", None))

        return possible_actions

    def make_decision(self, state):
        """
        The make_decision method implements the Expectiminimax algorithm for the AI Agent.
        The Expectiminimax algorithm is a recursive algorithm used for decision making.
        """
        # create a list of all possible actions the agent can take, from:
        # ["buy", "sell", "upgrade", "use_jail_card", "trade", "nothing_just_stay"]
        actions = self.current_possible_actions(state)

        # calculate the expected value for each action using expectiminimax algorithm
        action_values = []
        for action in actions:
            # apply the action to the game state to get the new state
            new_state = self.get_next_state(state, action)

            # calculate the expected value for the new state
            value = self.expectiminimax(new_state, self.depth)

            # add the action and its expected value to the list of action values
            action_values.append((action, value))

        # sort the actions by their expected values in descending order
        sorted_actions = sorted(action_values, key=lambda x: x[1], reverse=True)

        # choose the action with the highest expected value
        best_action = sorted_actions[0][0]

        # return the chosen action
        return best_action

    def expectiminimax(self, state, depth):
        """
        The expectiminimax method calculates the expected value of the given state using the Expectiminimax algorithm.
        """
        # check if the game is over or the maximum depth has been reached
        if state.is_terminal() or depth == 0:
            return self.evaluate_state(state)

        # check if it's the AI Agent's turn
        if state.get_self() == self:
            # maximize the expected value
            max_value = -np.inf
            actions = self.current_possible_actions(state)
            for action in actions:
                new_state = self.get_next_state(state, action)
                value = self.expectiminimax(new_state, depth - 1)
                max_value = max(max_value, value)
            return max_value

        # otherwise, it's the chance player's turn
        else:
            # calculate the expected value
            total_value = 0
            probabilities = state.get_chance_probabilities()
            for outcome, probability in probabilities.items():
                new_state = self.get_next_state(state, outcome)
                value = self.expectiminimax(new_state, depth - 1)
                total_value += value * probability
            return total_value

    def evaluate_state(self, state):
        """
        The evaluate_state method evaluates the given state and returns a score.
        """
        # implement your evaluation function here
        return random.randint(0, 100)
        best_value = -np.inf
        best_action = None
        for action in self.actions(dice1, dice2):
           pass
        return best_action

#TODO_: complete this
'''
def auction(player1, player2):
    # Check if both players agree to exchange the cities
    if players[0].agree_to_exchange(cities) and players[1].agree_to_exchange(cities):
        
        # Exchange the ownership of the cities
        players[0].remove_city(cities[0])
        players[1].add_city(cities[0])
        players[1].remove_city(cities[1])
        players[0].add_city(cities[1])
        
        print("The cities were exchanged between the players.")
        
    else:
        print("The players did not agree to exchange the cities.")
'''
