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
from monopoly_classes import *
from monopoly_AI_agent import *

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
def play_monopoly(players_num=2, AI_Agent_Mode=False, max_rounds=60):
        # ----------------      start game    ---------------- #
    round = 0
    while input("Inter \"c\" to continue or \"end\" to end this game: ") != "end" and round < max_rounds:
        for i in range(players_num):
            if players[i].is_bankrupt():
                print(f"{players[i].name} is bankrupt")
                players_num -= 1
                if players_num == 1:
                    print(f"{players[i].name} is the winner")
                    break
                continue
            # TODO_: Complete AI Agent Mode
            if AI_Agent_Mode:
                print(f"AI Agent is playing for {players[i].name}")
                AI_Agent(players[i])
                pass
            else:
                print(f"{players[i].name}'s turn")
                d1, d2, roll_result = dices.roll_double_dice()
                if d1 == d2:
                    if players[i].doubles_rolls > 2:
                        players[i].jail = True
                        players[i].doubles_rolls = 0
                        print(f"{players[i].name} went to jail becouse of 3 doubles rolls.")
                        continue
                    players[i].doubles = True
                    players[i].doubles_rolls += 1
                print(f"{players[i].name} rolled {d1} and {d2}")
                players[i].move(roll_result)
                print(f"{players[i].name} is on {properties[players[i].position].name}")
                
                if properties[players[i].position].type == "city" or properties[players[i].position].type == "service_centers":
                    if properties[players[i].position].owner != None and properties[players[i].position].owner != players[i]:
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
                if properties[players[i].position].type == "stay_place":
                    if properties[players[i].position].name == "Go (Collect $200)":
                        players[i].money += 200
                        print(f"{players[i].name} collected $200 from the bank for passing Go.")
                    elif properties[players[i].position].name == "Jail":
                        players[i].position = 10
                        players[i].jail = True
                        players[i].jail_turns += 1
                        print(f"{players[i].name} went to jail.")
                    elif properties[players[i].position].name == "Auction (Trade)":
                        pass
                    elif properties[players[i].position].name == "Free Parking":
                        pass
                    elif properties[players[i].position].name == "Chance":
                        pass
                    elif properties[players[i].position].name == "Income Tax":
                        players[i].money -= 0.1 * players[i].money
                        print(f"{players[i].name} paied ${0.1 * players[i].money} to the bank for Income Tax!")
                    elif properties[players[i].position].name == "Luxury Tax":
                        players[i].money -= 200
                        print(f"{players[i].name} paied $200 to the bank for Luxury Tax!")
                    elif properties[players[i].position].name == "Treasure":
                        rand_mony = random.randint(1, 10)*10
                        print(f"{players[i].name} got ${rand_mony} from the bank!")
                        players[i].money += rand_mony

                print("GAME STATE till now: ")
                print(f"| {players[i].name} has {players[i].doubles_rolls} doubles rolls")
                print(f"| {players[i].name} {'doubles' if players[i].jail else 'not doubles'} roll ({d1}, {d2})")
                print(f"| {players[i].name} has ${players[i].money} money left")
                print(f"| {players[i].name} has {players[i].properties} properties")
                print(f"| {players[i].name} has ${players[i].properties_value} properties value")
                print(f"| {players[i].name} has {players[i].countries} countries")
                print(f"| {players[i].name} is on {players[i].position} position")
                print(f"| {players[i].name} has {players[i].jail_cards} jail cards")
                print(f"| {players[i].name} is {'in' if players[i].jail else 'not in'} jail")
                print(f"| {players[i].name} has {players[i].jail_turns} jail turns")
                print(f"| {players[i].name} is {'bankrupt' if players[i].is_bankrupt() else 'not bankrupt'}")

                if players[i].jail_turns > 0:
                    players[i].jail_turns -= 1
                    players[i].jail = False
                if players[i].doubles == True:
                    print(f"{players[i].name} rolled double ({d1}, {d2}), his/her turn again!")
                    players[i].doubles = False
            
        print(f"\n--------------- ROUND {round+1} / {max_rounds} END ---------------\n")
        round += 1      

dices = DoubleDice()
        # ----------------  defining properties  ---------------- #
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
                                property_rent[i]))

if __name__ == "__main__":
        # ----------------  defining players  ---------------- #
    players_num = int(input(f"Enter the number of players (2 or 4): "))
    if players_num == 2 or players_num == 4:
        players = []
        AI_Agent_Mode = False
        for i in range(players_num):
            name = input(f"Enter the name of player {i+1} : ")
            if name == "AI" or name == "AI Agent" or name == "Agent":
                AI_Agent_Mode = True            
            players.append(Player(name))
    else:
        print("Number of players must be 2 or 4!")
        pass
        # ----------------       play       ---------------- #
    play_monopoly(players_num)
