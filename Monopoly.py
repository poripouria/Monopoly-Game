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
        if mode == "game":
            print("              +++++++++++++++++++++  GAME INFO  +++++++++++++++++++++ ")
            print(f"ROUND: {self.round+1} / {self.max_rounds}, MAX MONEY TO WIN: {self.max_money}") 
            print(f"PLAYERS ({self.players_num}):")     
            if self.round == 0:  
                for i, p in enumerate(self.players):
                    print(f"Player: {i+1}, Name: {p.name}, Money: {p.money}, type: {type(p).__name__}")
            else:   
                for i, p in enumerate(self.players):
                    print(f"Player: {i+1}, Name: {p.name}, Money: {p.money}, Currently on: ({self.properties[p.position].name}:{p.position})", end=" ")
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

    def start_game(self):
    # ----------------      start game    ---------------- #n
        random.shuffle(self.players)
        self.display_game_state()
        wtd = "c"
        while self.round < self.max_rounds and wtd != "end":
            if wtd == "g":
                self.display_game_state()
            elif wtd == "p":
                self.display_game_state("properties")
            for turn_counter in range(self.players_num):
            # ----------------  Check Current Player  ---------------- #
                current_player = self.players[turn_counter]
                if current_player.is_bankrupt():
                    print(f"{current_player.name} is bankrupt!")
                    self.players_num -= 1
                    self.players.remove(current_player)
                    self.losers.append(current_player)
                    if self.players_num == 1:
                        self.winner = self.players[0]
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
                    continue
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
            wtd = input("*** GAME MENU \n" +
                        "*** Inter \"c\" to continue \n" +
                        "*** Inter \"g\" to see game status \n" +
                        "*** Inter \"p\" to see properties status \n" +
                        "*** Inter \"end\" to END this game: ")
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
            current_player.play(self.properties[current_player.position], state=None)
        if type(current_player).__name__ == "Player":
            current_player.play(self.properties[current_player.position])
    # ---------------- Show Game Status  ---------------- #
        print(" _________________________ GAME STATUS TILL NOW: _________________________ ")
        self.display_game_state("players")
