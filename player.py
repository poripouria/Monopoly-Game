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
        self.jail_cards = 0
        self.jail_turns = 0
        self.doubles = False
        self.doubles_rolls = 0
        
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
            "Null"]
        command = random.choice(commands)
        print("Command is: " + command)
        if command == "Go to Jail for 2 rounds":
            self.jail = True
            self.jail_turns = 2
        elif command == "Pay $50 to all players":
            for player in players:
                if player != self:
                    player.money += 50
                    self.money -= 50
        elif command == "Give $20 from all players":
            for player in players:
                if player != self:
                    player.money -= 20
                    self.money += 20
        elif command == "Get 1 Jail-Free card":
            self.jail_cards += 1
        elif command == "Roll the dice again":
            self.doubles = True
        elif command == "Null":
            pass
        else:
            raise Exception("Something went wrong with the chance command")

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
        if property.country in self.countries:
            self.countries.remove(property.country)
        self.money += 0.8 * property.price

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
    def __init__(self, name, appearance=None, money=1500, depth=5):
        super().__init__(name, appearance, money)
        self.depth = depth

    def expectimax(self, state, depth):
        if depth == 0:
            # evaluate the state statically
            return self.evaluate(state)

        if state.is_terminal:
            return state.utility(self)

        if state.current_player == self:
            # maximize by picking the best action
            value = float('-inf')
            for action in state.actions():
                child_state = state.result(action)
                v = self.expectimax(child_state, depth)
                value = max(value, v)
            return value
        else:
            # expected value by averaging over all possible actions
            value = 0
            count = 0
            for action in state.actions():
                child_state = state.result(action)
                v = self.expectimax(child_state, depth - 1)
                value += v
                count += 1
            return value / count

    def evaluate(self, state):
        # basic static evaluation function that only considers the amount of money the player has
        return self.money

    def play(self, state):
        best_value = float('-inf')
        best_action = None
        for action in state.actions():
            child_state = state.result(action)
            value = self.expectimax(child_state, self.depth)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action

class AI_Agent_MiniMax(Player):
    def __init__(self, name, appearance=None, money=1500, depth=5):
        super().__init__(name, appearance, money)
        self.depth = depth

    def minimax(self, state, depth, is_maximizing):
        if depth == 0 or state.is_game_over():
            return state.evaluate_state(), None

        if is_maximizing:
            best_value = -np.inf
            best_move = None
            for move in state.get_possible_moves(self):
                new_state = state.get_new_state(move, self)
                move_value, _ = self.minimax(new_state, depth - 1, False)
                if move_value > best_value:
                    best_value = move_value
                    best_move = move
            return best_value, best_move
        else:
            best_value = np.inf
            best_move = None
            for move in state.get_possible_moves(self):
                new_state = state.get_new_state(move, self)
                move_value, _ = self.minimax(new_state, depth - 1, True)
                if move_value < best_value:
                    best_value = move_value
                    best_move = move
            return best_value, best_move

    def make_move(self, state):
        _, best_move = self.minimax(state, self.depth, True)
        return best_move


    def move(self, player, properties, players):
        """
        Choose the optimal action for a player in a Monopoly game 
        using the ExpectMinMax algorithm. Here the agent plays to 
        maximize its profits.
        """
        actions = self.get_legal_moves(player, properties)
        _, action = self.expectimax_decision(player, properties, players, 0, True)
        assert action in actions
        self.do_action(player, properties, action, players)

    def expectimax_decision(self, player, properties, players, depth, maximizing_player):
        """
        Returns the optimal action to take for a player using 
        the Expectimax algorithm.
        """
        if player.is_bankrupt():
            return -np.inf, None
        
        if depth == self.depth:
            return self.calc_board_utility(player, properties), None

        if maximizing_player:
            v_max = -np.inf
            best_action = None
            for action in self.get_legal_moves(player, properties):
                copy_player = player.copy()
                copy_properties = self.get_copy_properties(properties)
                copy_players = self.get_copy_players(players)
                self.do_action(copy_player, copy_properties, action, copy_players)
                v, _ = self.expectimax_decision(copy_player, copy_properties, copy_players, depth + 1, False)
                if v > v_max:
                    v_max, best_action = v, action
            return v_max, best_action
            
        else:
            v_exp = 0
            actions = self.get_legal_moves(player, properties)
            for action in actions:
                copy_player = player.copy()
                copy_properties = self.get_copy_properties(properties)
                copy_players = self.get_copy_players(players)
                self.do_action(copy_player, copy_properties, action, copy_players)
                v, _ = self.expectimax_decision(copy_player, copy_properties, copy_players, depth + 1, True)
                v_exp += v / len(actions)
            return v_exp, None
        
    def get_legal_moves(self, player, properties):
        """
        Returns all legal moves for a player in a Monopoly game.
        """
        moves = []
        dices = DoubleDice()
        d1, d2, roll_result = dices.roll_double_dice()  
        if player.jail and player.jail_cards > 0:
            moves.append('use jail card')
        elif player.jail:
            moves.append('do nothing')
        else:
            moves.append('end turn')
            if d1 == d2:
                moves.append('roll dice again')
                if player.doubles_rolls < 2:
                    moves.append('move')
            else:
                moves.append('move')
        return moves

    def do_action(self, player, properties, action, players):
        """
        Performs the given action for the agent. Here agent 
        receives utility for moving to other tiles and receives 
        rewards for collecting rent for its owned tiles.
        """
        if action == 'use jail card' and player.jail_cards > 0:
            player.jail = False
            player.jail_cards -= 1
        elif action == 'do nothing':
            player.jail_turns += 1
        elif action == 'end turn':
            player.jail_turns = max(0, player.jail_turns - 1)
        elif action == 'move':
            dices = DoubleDice()
            d1, d2, roll_result = dices.roll_double_dice()  
            player.move(roll_result)
            if properties[player.position].owner and properties[player.position].owner != player:
                player.pay_rent(properties[player.position])
            elif player.money > properties[player.position].price * 1.1:
                player.buy_property(properties[player.position])
        elif action == 'roll dice again':
            player.move(d1+d2)
            player.doubles_rolls += 1
            if properties[player.position].owner and properties[player.position].owner != player:
                player.pay_rent(properties[player.position])
            elif player.money > properties[player.position].price * 1.1:
                player.buy_property(properties[player.position])
        else:
            raise Exception('Invalid action')

    def calc_board_utility(self, player, properties):
        """
        Evaluates the game utility for each player in a game. Here the agent 
        evaluates the sum of its tile property values minus the sum of its 
        players debts.
        """
        utility = 0
        for p in properties:
            if p.owner == player:
                utility += p.price
        utility -= player.get_debt()
        return utility
    
    def get_copy_properties(self, properties):
        """
        Returns a deepcopy of a list of properties.
        """
        copy_properties = []
        for p in properties:
            copy_properties.append(p.copy())
        return copy_properties

    def get_copy_players(self, players):
        """
        Returns a deepcopy of a list of players.
        """
        copy_players = []
        for player in players:
            copy_players.append(player.copy())
        return copy_players
