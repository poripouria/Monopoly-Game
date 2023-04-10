"""
Description:
    Monopoly game (2 players) and AI Agent
    Project for Amirkabir University of Technilogy (Tehran Polytechnic)
    Computer Scince department
    Artificial Inteligence Course

Student Name & ID: Pouria Alimoradpor 9912035
"""
import random
import numpy as np
import pandas as  pd
from Player import Player, AI_Agent
from Monopoly import *

try:
    if __name__ == "__main__":
        # ----------------   defining players  ---------------- #
        players_num = int(input(f"Enter the number of players (2 - 3 - 4): "))
        if players_num in [2, 3, 4]:
            players = []
            AI_Mode = False
            for i in range(players_num):
                name = input(f"Enter the name of player {i+1} (Any Name / AI): ")
                if name == "AI":
                    AI_Mode = True    
                    players.append(AI_Agent(name + "_" + str(i+1)))
                else:
                    players.append(Player(name))
        else:
            raise Exception("Number of players must be 2, 3 or 4!")
        Monopoly_Game = Monopoly(players, players_num, AI_Agent_Mode = AI_Mode)
        # ---------------- defining properties ---------------- #
        df = pd.read_excel("_Data/Properties-Detail.xlsx")
        Monopoly_Game.init_board(df)
        # ----------------        start        ---------------- #
        Monopoly_Game.start_game()
except Exception as err :
    print(err)
