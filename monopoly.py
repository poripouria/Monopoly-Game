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

class Monopoly():
    def __init__(self, players, properties, players_num=2, AI_Agent_Mode=False, max_rounds=40):
        self.players = players
        self.properties = properties
        self.players_num = players_num
        self.AI_Agent_Mode = AI_Agent_Mode
        self.max_rounds = max_rounds
        self.round = 0
        self.losers = []
        self.winner = None

    def game_state(self):
        pass

    def current_possible_moves(self):
        pass

    def display_game_state(self, mode="players"):
        match mode:
            case "properties":
                print("                     +++++++++++++++++++++ PROPERTIES +++++++++++++++++++++ ")
                for p in self.properties:
                    p.print_property_status()
            case  "players":
                print("                     +++++++++++++++++++++   PLAYERS  +++++++++++++++++++++ ")
                for p in self.players:
                    p.print_player_status()
            case _:
                raise Exception("Something went wrong in DISPLAYING GAME STATUS.")

    def start_game(self):
            # ----------------      start game    ---------------- #
        wtd = "c"
        match wtd:
            case "c":
                while self.round < self.max_rounds and wtd != "end":
                    if self.AI_Agent_Mode:
                        for i, p in enumerate(self.players):
                            print(f"Player {i+1}: Name: {p.name}, is {type(p).__name__}")

                    for turn_counter in range(self.players_num):
                        current_player = self.players[turn_counter]
                        if current_player.is_bankrupt():
                            print(f"{current_player.name} is bankrupt!")
                            self.players_num -= 1
                            self.players.remove(current_player)
                            if players_num == 1:
                                print(f"{players} is the WINNER")
                                return
                        if current_player.jail and current_player.jail_turns > 0:
                            current_player.doubles = False
                            current_player.doubles_rolls = 0
                            current_player.jail_turns -= 1
                            if current_player.jail_turns == 0:
                                current_player.jail = False
                        """if current_player.jail:
                            current_player.jail_turns -= 1
                            if current_player.jail_turns == 0:
                                current_player.jail = False
                            continue"""
                        self.play_monopoly(current_player)
                        if current_player.doubles:
                            self.play_monopoly(current_player)
                            if current_player.doubles:
                                self.play_monopoly(current_player)
                                if current_player.doubles:
                                    self.play_monopoly(current_player)
                    print(f"\n--------------- ROUND {self.round+1} / {self.max_rounds} END ---------------\n")
                    wtd = input("*** Inter \"c\" to continue \n" +
                                "*** Inter \"p\" to see properties status \n" +
                                "*** Inter \"end\" to END this game: ")
                    if wtd == "p":
                        self.display_game_state("properties")
                        wtd = "c"
                    self.round += 1
            case "end":
                print("Game END.")
                return
            case _:
                wtd = "c"

    def play_monopoly(self, current_player):
            # ----------------     Roll Dices   ---------------- #
        print(f"\n{current_player.name}'s turn")
        dices = DoubleDice()
        d1, d2, roll_result = dices.roll_double_dice()
        if d1 == d2:
            if current_player.doubles_rolls > 2:
                current_player.jail = True
                current_player.doubles_rolls = 0
                print(f"{current_player.name} went to jail becouse of 3 doubles rolls.")
                pass
            if current_player.jail:
                current_player.jail_turns -= 1
                print(f"{current_player.name} is still in jail and couldn't roll again.")
                pass
            current_player.doubles = True
            current_player.doubles_rolls += 1
        else:
            current_player.doubles = False
            current_player.doubles_rolls = 0
        print(f"{current_player.name} rolled {d1} and {d2}")
        current_player.move(roll_result)
        print(f"{current_player.name} is on {self.properties[current_player.position].name}")
            # ----------------  Players Decision ---------------- #
        if type(current_player).__name__ == "AI_Agent":
            current_player.play(d1, d2)
        if type(current_player).__name__ == "Player":
            if self.properties[current_player.position].type == "city" or self.properties[current_player.position].type == "service_centers":
                if self.properties[current_player.position].owner != None and self.properties[current_player.position].owner != current_player:
                    print(f"{current_player.name} has to pay ${self.properties[current_player.position].rent} to {self.properties[current_player.position].owner.name}")
                    current_player.pay_rent(self.properties[current_player.position])
                elif self.properties[current_player.position].owner == None:
                    print(f"{current_player.name} can buy {self.properties[current_player.position].name} for ${self.properties[current_player.position].price}")
                    if input(f"Do you want to buy it (you have ${current_player.money})? (y/n) ") == "y":
                        if current_player.money < self.properties[current_player.position].price:
                            print("You don't have enough money to buy it") 
                        else:
                            print(f"You bought {self.properties[current_player.position].name}.")
                            current_player.buy_property(self.properties[current_player.position])
                    else:
                        print(f"You didn't buy {self.properties[current_player.position].name}.")
                        pass
                elif self.properties[current_player.position].owner == current_player:
                    if input(f"Do you want to sell {self.properties[current_player.position].name} for {0.8 * self.properties[current_player.position].price}? (y/n) ") == "y":
                        print(f"You soled {self.properties[current_player.position].name} for {0.8 * self.properties[current_player.position].price}.")
                        current_player.sell_property(self.properties[current_player.position])
                    else:
                        print(f"You didn't sell {self.properties[current_player.position].name}.")
                        pass
            if self.properties[current_player.position].type == "stay_place":
                if self.properties[current_player.position].name == "Go (Collect $200)":
                    pass
                elif self.properties[current_player.position].name == "Jail":
                    if current_player.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                        current_player.jail_cards -= 1
                        current_player.jail = False
                        print(f"{current_player.name} used a get out of jail free card.")
                    current_player.position = 10
                    current_player.jail = True
                    current_player.jail_turns += 2
                    print(f"{current_player.name} went to jail.")
                elif self.properties[current_player.position].name == "Auction (Trade)":
                    #TODO_: After compliting auction function, add it here
                    print("Currently Auction (Trade) is not available!")
                    pass
                elif self.properties[current_player.position].name == "Free Parking":
                    pass
                elif self.properties[current_player.position].name == "Chance":
                    current_player.chance(self.players)
                elif self.properties[current_player.position].name == "Income Tax":
                    print(f"{current_player.name} paied ${0.1 * current_player.money} to the bank for Income Tax!")
                    current_player.money -= 0.1 * current_player.money
                elif self.properties[current_player.position].name == "Luxury Tax":
                    current_player.money -= 200
                    print(f"{current_player.name} paied $200 to the bank for Luxury Tax!")
                elif self.properties[current_player.position].name == "Treasure":
                    rand_mony = random.randint(1, 10)*10
                    print(f"{current_player.name} got ${rand_mony} from the bank!")
                    current_player.money += rand_mony
                else:
                    raise Exception("Something went wrong in STAY_PLACE POSITIONS.")

        print(" _________________________ GAME STATUS TILL NOW: _________________________ ")
        self.display_game_state()

        if current_player.jail and current_player.jail_turns > 0:
            current_player.doubles = False
            current_player.doubles_rolls = 0
            current_player.jail_turns -= 1
            if current_player.jail_turns == 0:
                current_player.jail = False
        elif current_player.jail_turns == 0 and  current_player.doubles:
                print(f"{current_player.name} rolled double ({d1}, {d2}), his/her turn again!")
