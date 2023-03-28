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

def play_monopoly(players_num=2, max_rounds=60, AI_Agent_Mode=False):
        # ----------------  defining properties  ---------------- #
    property_place = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for place in df["place"]:
        property_place.append(place)
    property_type = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for type in df["type"]:
        property_type.append(type)
    property_country = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for country in df["country"]:
        property_country.append(country)
    property_price = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for price in df["price"]:
        property_price.append(price)
    property_rent = []
    df = pd.read_excel("_Data/Properties-Detail.xlsx")
    for rent in df["rent"]:
        property_rent.append(rent)

    properties = []
    for i in range(40):
        properties.append(Property(property_place[i], 
                                    property_type[i], 
                                    property_country[i], 
                                    property_price[i], 
                                    property_rent[i]))

        # ----------------  defining players  ---------------- #
    players = []
    for i in range(players_num):
        name = input(f"Enter the name of player {i+1} : ")
        if name == "AI" or name == "AI Agent":
            AI_Agent_Mode = True            
        players.append(Player(name))

        # ----------------  start game  ---------------- #
    while input("Inter \"c\" to continue or \"end\" to exit: ") != "end":
        for i in range(players_num):
            if players[i].is_bankrupt():
                continue
            if AI_Agent_Mode:
                print(f"AI Agent is playing for {players[i].name}")
                AI_Agent(players[i])
            else:
                print(f"{players[i].name}'s turn")
                d1, d2, roll_result = dices.roll_double_dice()
                print(f"{players[i].name} rolled {d1} and {d2}")
                players[i].move(roll_result)
                print(f"{players[i].name} is on {properties[players[i].position].name}")
                if properties[players[i].position].owner != None:
                    print(f"{players[i].name} has to pay ${properties[players[i].position].rent} to {properties[players[i].position].owner.name}")
                    players[i].pay_rent(properties[players[i].position])
                else:
                    print(f"{players[i].name} can buy {properties[players[i].position].name} for ${properties[players[i].position].price}")
                    if input(f"Do you want to buy it (you have ${players[i].money})? (y/n) ") == "y":
                        if players[i].money < properties[players[i].position].price:
                            print("You don't have enough money to buy it") 
                        else:
                            players[i].buy_property(properties[players[i].position])
                    else:
                        pass

                print("GAME STATE till now: ")
                print(f"{players[i].name} has {players[i].doubles_rolls} doubles rolls")
                print(f"{players[i].name} has ${players[i].money} money left")
                print(f"{players[i].name} has {players[i].properties} properties")
                print(f"{players[i].name} has ${players[i].properties_value} properties value")
                print(f"{players[i].name} has {players[i].countries} countries")
                print(f"{players[i].name} is on {players[i].position} position")
                print(f"{players[i].name} is {'in' if players[i].jail else 'not in'} jail")
                print(f"{players[i].name} has {players[i].jail_cards} jail cards")
                print(f"{players[i].name} has {players[i].jail_turns} jail turns")
                print(f"{players[i].name} is {'bankrupt' if players[i].is_bankrupt() else 'not bankrupt'}")
                # print(players, "\n", properties, "\n")

if __name__ == "__main__":
    play_monopoly()
