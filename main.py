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
from Monopoly import *
from Player import Player, AI_Agent
from Property import *

try:
    if __name__ == "__main__":
    # ---------------- defining properties ---------------- #
        df = pd.read_excel("_Data/Properties-Detail.xlsx")
        property_place = []
        for place_ in df["place"]:
            property_place.append(place_)
        property_type = []
        for type_ in df["type"]:
            property_type.append(type_)
        property_country = []
        for country_ in df["country"]:
            property_country.append(country_)
        property_price = []
        for price_ in df["price"]:
            property_price.append(price_)
        property_rent = []
        for rent_ in df["rent"]:
            property_rent.append(rent_)
        properties = []
        for i in range(40):
            properties.append(Property(property_place[i], 
                                        property_type[i], 
                                        property_country[i], 
                                        property_price[i], 
                                        property_rent[i], i))
    # ----------------   defining players  ---------------- #
        players_num = int(input(f"Enter the number of players (2 - 3 - 4): "))
        if players_num == 2 or players_num == 3 or players_num == 4:
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
        
    # ----------------         play        ---------------- #
        Monopoly(players, properties, players_num, AI_Agent_Mode = AI_Mode).start_game()
except Exception as err :
    print(err)
