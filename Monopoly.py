"""
Description: Game board and rules
"""

import random
from Property import *

class Monopoly():
    def __init__(self, players, players_num=2, max_rounds=30, max_money=3000, AI_Agent_Mode=False):
        self.players = players
        self.properties = []
        self.players_num = players_num
        self.max_rounds = max_rounds
        self.max_money = max_money
        self.AI_Agent_Mode = AI_Agent_Mode
        self.round = 0
        self.turn_counter = -1
        self.current_player = None
        self.losers = []
        self.winner = None
        self.whattodo = "c"

    def init_board(self, df):
        properties = []
        for i in range(40):
            properties.append(Property(df.iloc[i]["place"],
                                       df.iloc[i]["type"],
                                       df.iloc[i]["country"],
                                       float(df.iloc[i]["price"]),
                                       float(df.iloc[i]["rent"]),
                                       int(i)))
        self.properties = properties

    def start_game(self):
        # ----------------      start game    ---------------- #
        random.shuffle(self.players)
        self.display_game_state()
        self.show_game_menu()
        while self.round < self.max_rounds and self.whattodo != "end":          # End of game
            if self.whattodo == "g": self.display_game_state()                  # Game status
            elif self.whattodo == "p": self.display_game_state("properties")    # Properties status
            for turn_counter in range(self.players_num):
                # ----------------  Check Current Player  ---------------- #
                current_player = self.players[turn_counter]
                self.turn_counter = turn_counter
                self.current_player = current_player
                if current_player.is_bankrupt():
                    print(f"{current_player.name} is bankrupt!")
                    for p in current_player.properties:
                       p.owner = None
                    self.players_num -= 1
                    self.losers.append(current_player)
                    self.players.remove(current_player)
                if self.players_num == 1:
                    self.winner = self.players[0]
                    self.display_game_state()
                    print("\n", "ALL OTHER PLAYERS ARE BANKRUPT!")
                    print(f"#### WINNER: {self.winner.name}")
                    print(f"#### LOSERS: {self.losers}")
                    return
                if current_player.jail and current_player.jail_turns > 0:
                    current_player.doubles = False
                    current_player.doubles_rolls = 0
                    current_player.jail_turns -= 1
                    print(f"\n{current_player.name} is in JAIL and can't roll dices.")
                    if current_player.jail_turns == 0:
                        current_player.jail = False
                    continue
                print(f"\n{current_player.name}'s turn")
                for i in range(4):
                    # ----------------     Roll Dices    ---------------- #
                    if type(current_player).__name__ == "Player":
                        input("*** Press Inter to ROLL DICES.")
                    current_player.roll_dices()
                    print(f"{current_player.name} is on {self.properties[current_player.position].name}.")
                    # ----------------  Players Decision ---------------- #
                    if type(current_player).__name__ == "AI_Agent":
                        current_player.play(current_player.position, self.game_state())
                    if type(current_player).__name__ == "Player":
                        current_player.play(current_player.position, self.game_state())
                    # ---------------- Show Players Status  ---------------- #
                    print(" _________________________ GAME STATUS TILL NOW: _________________________ ")
                    self.display_game_state("players")
                    if not current_player.doubles:
                        break
            # ----------------    Show Game State    ---------------- #
            self.check_winner()
            print(f"\n--------------- ROUND {self.round+1} / {self.max_rounds} END ---------------\n")
            self.round += 1
            self.show_game_menu()
        self.check_winner()
        self.display_game_state()
        print("\n", "Game END.")
        print(f"#### WINNER: {self.winner.name}")
        print(f"#### LOSERS: {self.losers}", "\n")
        return
        
    def check_winner(self):
        richest = max(self.players, key=lambda p: p.wealth)
        if richest.wealth >= self.max_money:
            self.winner = richest
            print(f"{self.winner.name} is the winner with {self.winner.wealth} wealth!")
            self.whattodo = "end"
        else:
            self.losers = sorted(self.players, key=lambda p: (p.wealth, p.money), reverse=True)
            self.winner = self.losers.pop(0)

    def game_state(self):
        state = {"properties": self.properties,
                 "players": self.players,
                 "players_num": self.players_num,
                 "rounds_left": self.max_rounds - self.round,
                 "turn_counter": self.turn_counter,
                 "current_player": self.current_player,
                 "winner": self.winner,
                 "max_money": self.max_money}
        return state

    def display_game_state(self, mode="game"):
        if mode == "game":
            print("              +++++++++++++++++++++  GAME INFO  +++++++++++++++++++++ ")
            print(f"ROUND: {self.round+1} / {self.max_rounds}, MAX MONEY TO WIN: {self.max_money}") 
            print(f"PLAYERS ({self.players_num}):")     
            if self.round == 0:  
                for i, p in enumerate(self.players):
                    print(f"Player: {i+1}, Name: {p.name}, Wealth: {p.wealth}, type: {type(p).__name__}")
            else:   
                for i, p in enumerate(self.players):
                    print(f"Player: {i+1}, Name: {p.name}, Wealth: {p.wealth}, Currently on: ({self.properties[p.position].name}:{p.position})", end=" ")
                    if p == self.winner:
                        print("(WINNER TILL NOW)", end=" ")
                    print()
        elif mode == "properties":
            print("               +++++++++++++++++++++ PROPERTIES +++++++++++++++++++++ ")
            for p in self.properties:
                p.print_property_status()
        elif mode == "players":
            print("               +++++++++++++++++++++   PLAYERS  +++++++++++++++++++++ ")
            for p in self.players:
                p.print_player_status(self.properties)
        else:
            raise Exception("Something went wrong in DISPLAYING GAME STATUS.")
        print()

    def show_game_menu(self):
        self.whattodo = input("*** GAME MENU \n" +
                              "*** Inter \"c\" to continue \n" +
                              "*** Inter \"g\" to see game status \n" +
                              "*** Inter \"p\" to see properties status \n" +
                              "*** Inter \"end\" to END this game: ")    
