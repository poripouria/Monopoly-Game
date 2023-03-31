import random
import numpy as np

class Monopoly():
    def __init__(self, players, properties, players_num=2, max_rounds=30, max_money=3500, AI_Agent_Mode=False):
        self.players = players
        self.properties = properties
        self.players_num = players_num
        self.max_rounds = max_rounds
        self.max_money = max_money
        self.AI_Agent_Mode = AI_Agent_Mode
        self.round = 0
        self.losers = []
        self.winner = None

    def current_possible_moves(self):
        pass

    def check_winner(self):
        richest = None
        richestmoney = -np.inf
        for p in self.players:
            if p.money == self.max_money:
                self.winner = p
            elif p.money > richestmoney:
                richest = p
                richestmoney = p.money
        self.winner = richest
        self.losers = self.players[:]
        self.losers.remove(self.winner)

    def display_game_state(self, mode="game"):
        match mode:
            case "properties":
                print("               +++++++++++++++++++++ PROPERTIES +++++++++++++++++++++ ")
                for p in self.properties:
                    p.print_property_status()
            case  "players":
                print("               +++++++++++++++++++++   PLAYERS  +++++++++++++++++++++ ")
                for p in self.players:
                    p.print_player_status()
            case  "game":
                if self.round == 0:
                    print("               +++++++++++++++++++++  GAME INFO  +++++++++++++++++++++ ")
                    print(f"ROUND: {self.round+1} / {self.max_rounds}, MAX MONEY TO WIN: {self.max_money}")    
                    print(f"PLAYERS ({self.players_num}):")    
                    for i, p in enumerate(self.players):
                        print(f"Player: {i+1}, Name: {p.name}, Money: {p.money}, type: {type(p).__name__}")

                else:
                    print("               +++++++++++++++++++++  GAME INFO  +++++++++++++++++++++ ")
                    print(f"ROUND: {self.round+1} / {self.max_rounds}, MAX MONEY TO WIN: {self.max_money}")    
                    print(f"PLAYERS ({self.players_num}):")    
                    for i, p in enumerate(self.players):
                        print(f"Player: {i+1}, Name: {p.name}, Money: {p.money}, Currently on: ({self.properties[p.position].name}:{p.position})", end=" ")
                        if p == self.winner:
                            print("(WINNER TILL NOW)", end=" ")
                        print()
                    print()
            case _:
                raise Exception("Something went wrong in DISPLAYING GAME STATUS.")

    def start_game(self):
    # ----------------      start game    ---------------- #
        random.shuffle(self.players)
        self.display_game_state()
        print()
        wtd = "c"
        while self.round < self.max_rounds and wtd != "end":
            wtd = input("*** GAME MENU \n" +
                        "*** Inter \"c\" to continue \n" +
                        "*** Inter \"g\" to see game status \n" +
                        "*** Inter \"p\" to see properties status \n" +
                        "*** Inter \"end\" to END this game: ")
            if wtd == "g":
                self.display_game_state()
            elif wtd == "p":
                self.display_game_state("properties")
            print()
            for turn_counter in range(self.players_num):
            # ----------------  Check Current Player  ---------------- #
                current_player = self.players[turn_counter]
                if current_player.is_bankrupt():
                    print(f"{current_player.name} is bankrupt!")
                    self.players_num -= 1
                    self.players.remove(current_player)
                    self.losers.append(current_player)
                    if self.players_num == 1:
                        self.winner = players[0]
                        print()
                        print(f"#### WINNER: {self.winner.name}")
                        print(f"#### LOSERS: {self.losers}")
                        return
                if current_player.jail and current_player.jail_turns > 0:
                    current_player.doubles = False
                    current_player.doubles_rolls = 0
                    current_player.jail_turns -= 1
                    print(f"{current_player.name} is in JAIL and can't roll dices.")
                    if current_player.jail_turns == 0:
                        current_player.jail = False
                    break
            # ----------------        Roll Dices      ---------------- #
                print(f"\n{current_player.name}'s turn")
                for i in range(4):
                    input("*** Press Inter to ROLL DICES.")
                    current_player.roll_dices()
                    self.play_monopoly(current_player)
                    if not current_player.doubles:
                        break
            # ----------------    Check Game State    ---------------- #
            self.check_winner()
            print(f"\n--------------- ROUND {self.round+1} / {self.max_rounds} END ---------------\n")
            self.round += 1
        self.check_winner()
        print()
        print("Game END.")
        print(f"#### WINNER: {self.winner.name}")
        print(f"#### LOSERS: {self.losers}")
        print()
        return

    def play_monopoly(self, current_player):
    # ----------------  Players Decision ---------------- #
        print(f"{current_player.name} is on {self.properties[current_player.position].name}")
        if type(current_player).__name__ == "AI_Agent":
            current_player.play()
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
                    else:
                        current_player.position = 10
                        current_player.jail = True
                        current_player.jail_turns += 1
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
    # ---------------- Show Game Status  ---------------- #
        print(" _________________________ GAME STATUS TILL NOW: _________________________ ")
        self.display_game_state("players")
