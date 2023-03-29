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


def display_game_state(players, properties=None):
    for current_player in players:
        print(f"| _____________{current_player.name}_____________")
        print(f"| {current_player.name} has {current_player.doubles_rolls} doubles rolls")
        print(f"| {current_player.name} has ${current_player.money} money left")
        print(f"| {current_player.name} has {current_player.properties} properties")
        print(f"| {current_player.name} has ${current_player.properties_value} properties value")
        print(f"| {current_player.name} has {current_player.countries} countries")
        print(f"| {current_player.name} is on {current_player.position} position")
        print(f"| {current_player.name} is {'in' if current_player.jail else 'not in'} jail")
        print(f"| {current_player.name} has {current_player.jail_turns} jail turns")
        print(f"| {current_player.name} has {current_player.jail_cards} jail cards")
        print(f"| {current_player.name} is {'bankrupt' if current_player.is_bankrupt() else 'not bankrupt'}")

def monopoly_game(players, properties, players_num=2, AI_Agent_Mode=False, max_rounds=60):
        # ----------------      start game    ---------------- #
    round = 0
    while round < max_rounds and input("Inter \"c\" to continue or \"end\" to end this game: ") != "end":
        # TODO_: Complete AI Agent Mode
        if AI_Agent_Mode:
            for i, p in enumerate(players):
                print(f"Player {i+1}: Name: {p.name}, is {type(p).__name__}")

        for turn_counter in range(players_num):
            current_player = players[turn_counter]
            if current_player.is_bankrupt():
                print(f"{current_player.name} is bankrupt")
                players_num -= 1
                for p in players:
                    if p != current_player:
                        p.money += current_player.money / (players_num - 1)
                players.remove(current_player)
                if players_num == 1:
                    print(f"{current_player.name} is the WINNER")
                    return
            if current_player.jail:
                break
            play_monopoly(current_player, players)
            if current_player.doubles:
                play_monopoly(current_player, players)
                if current_player.doubles:
                    play_monopoly(current_player, players)
                    if current_player.doubles:
                        play_monopoly(current_player, players)

        print(f"\n--------------- ROUND {round+1} / {max_rounds} END ---------------\n")
        round += 1

def play_monopoly(current_player, players):
    dices = DoubleDice()
    print(f"{current_player.name}'s turn")
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
    print(f"{current_player.name} is on {properties[current_player.position].name}")
    
    if properties[current_player.position].type == "city" or properties[current_player.position].type == "service_centers":
        if properties[current_player.position].owner != None and properties[current_player.position].owner != current_player:
            print(f"{current_player.name} has to pay ${properties[current_player.position].rent} to {properties[current_player.position].owner.name}")
            current_player.pay_rent(properties[current_player.position])
        else:
            print(f"{current_player.name} can buy {properties[current_player.position].name} for ${properties[current_player.position].price}")
            if input(f"Do you want to buy it (you have ${current_player.money})? (y/n) ") == "y":
                if current_player.money < properties[current_player.position].price:
                    print("You don't have enough money to buy it") 
                else:
                    print(f"You bought {properties[current_player.position].name}.")
                    current_player.buy_property(properties[current_player.position])
            else:
                print(f"You didn't buy {properties[current_player.position].name}.")
                pass
    if properties[current_player.position].type == "stay_place":
        if properties[current_player.position].name == "Go (Collect $200)":
            pass
        elif properties[current_player.position].name == "Jail":
            if current_player.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                current_player.jail_cards -= 1
                current_player.jail = False
                print(f"{current_player.name} used a get out of jail free card.")
            current_player.position = 10
            current_player.jail = True
            current_player.jail_turns += 1
            print(f"{current_player.name} went to jail.")
        elif properties[current_player.position].name == "Auction (Trade)":
            print("Currently Auction (Trade) is not available!")
            pass
        elif properties[current_player.position].name == "Free Parking":
            pass
        elif properties[current_player.position].name == "Chance":
            current_player.chance(players)
        elif properties[current_player.position].name == "Income Tax":
            print(f"{current_player.name} paied ${0.1 * current_player.money} to the bank for Income Tax!")
            current_player.money -= 0.1 * current_player.money
        elif properties[current_player.position].name == "Luxury Tax":
            current_player.money -= 200
            print(f"{current_player.name} paied $200 to the bank for Luxury Tax!")
        elif properties[current_player.position].name == "Treasure":
            rand_mony = random.randint(1, 10)*10
            print(f"{current_player.name} got ${rand_mony} from the bank!")
            current_player.money += rand_mony

    print(" _________________________ GAME PLAYERS STATUS TILL NOW: _________________________ ")
    display_game_state(players)

    if current_player.jail_turns > 0:
        current_player.jail_turns -= 1
        current_player.jail = False
    if current_player.doubles:
        print(f"{current_player.name} rolled double ({d1}, {d2}), his/her turn again!")

try:
    if __name__ == "__main__":
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
            # ----------------  defining players  ---------------- #
        players_num = int(input(f"Enter the number of players (2 or 4): "))
        if players_num == 2 or players_num == 4:
            players = []
            AI_Agent_Mode = False
            for i in range(players_num):
                name = input(f"Enter the name of player {i+1} : ")
                if name == "AI":
                    AI_Agent_Mode = True    
                    players.append(AI_Agent(name + "_" + str(i+1)))

                else:
                    players.append(Player(name))
        else:
            raise Exception("Number of players must be 2 or 4!")
        
            # ----------------       play       ---------------- #
        monopoly_game(players, properties, players_num, AI_Agent_Mode)
except Exception as err :
    print(err)
