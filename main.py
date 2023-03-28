"""
Description:
    Monopoly game (2 players) and AI Agent
    Project for Amirkabir University of Technilogy (Tehran Polytechnic)
    Computer Scince department
    Artificial Inteligence Course

Student Name & ID: Pouria Alimoradpor 9912035
"""
import numpy as np
import pandas as  pd
from monopoly_classes import *

AI_Agent_Mode = False
"""
def AI_Agent(player):
        if player.jail:
            if player.jail_cards > 0:
                player.jail_cards -= 1
                player.jail = False
            elif player.jail_turns < 3:
                player.jail_turns += 1
            else:
                player.money -= 50
                player.jail = False
                player.jail_turns = 0
        else:
            if player.doubles >= 3:
                player.jail = True
                player.doubles = 0
            else:
                d1, d2, roll_result = dices.roll_double_dice()
                player.move(roll_result)
                if d1 == d2:
                    player.doubles += 1
                else:
                    player.doubles = 0
                if property_place[player.position].owner:
                    player.pay_rent(property_place[player.position])
                else:
                    player.buy_property(property_place[player.position])
"""

dices = DoubleDice()

def play_monopoly(players_num=2, max_rounds=60):
    property_place = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for place in df["place"]:
        property_place.append(place)
    # print(property_place)
    property_type = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for type in df["type"]:
        property_type.append(type)
    # print(property_type)
    property_country = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for country in df["country"]:
        property_country.append(country)
    # print(property_country)
    property_price = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for price in df["price"]:
        property_price.append(price)
    # print(property_price)
    property_rent = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for rent in df["rent"]:
        property_rent.append(rent)
    # print(property_rent)

    players = []
    for i in range(players_num):
        name = input(f"Enter the name of player {i+1} : ")
        if name == "AI" or name == "AI Agent":
            AI_Agent_Mode = True            
        players.append(Player(name))
    # print(players)

    while True:
        for i in range(players):
            if player[i].is_bankrupt():
                continue
            if AI_Agent_Mode:
                print(f"AI Agent is playing for {player[i].name}")
                AI_Agent(player[i])
            else:
                print(f"{player[i].name}'s turn")
                d1, d2, roll_result = dices.roll_double_dice()
                player[i].move(roll_result)
                print(f"{player[i].name} is on {property_place[player[i].position].name}")
                if property_place[player[i].position].owner:
                    print(f"{player[i].name} has to pay {property_place[player[i].position].rent} to {property_place[player[i].position].owner.name}")
                    player[i].pay_rent(property_place[player[i].position])
                else:
                    print(f"{player[i].name} can buy {property_place[player[i].position].name} for {property_place[player[i].position].price}")
                    if input("Do you want to buy it? (y/n) ") == "y":
                        player[i].buy_property(property_place[player[i].position])
                print(f"{player[i].name} has {player[i].money} money left")
                print(f"{player[i].name} has {player[i].jail_cards} jail cards")
                print(f"{player[i].name} has {player[i].jail_turns} jail turns")
                print(f"{player[i].name} has {player[i].doubles} doubles")
                print(f"{player[i].name} has {player[i].doubles_rolls} doubles rolls")
                print(f"{player[i].name} has {player[i].properties} properties")
                print(f"{player[i].name} has {player[i].countries} countries")
                print(f"{player[i].name} has {player[i].properties_value} properties value")
                print(f"{player[i].name} is on {player[i].position} position")
                print(f"{player[i].name} is {'in' if player[i].jail else 'not in'} jail")
                print(f"{player[i].name} is {'bankrupt' if player[i].is_bankrupt() else 'not bankrupt'}")

if __name__ == "__main__":
    play_monopoly()
