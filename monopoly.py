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

def display_game_state(players, properties):
    for p in players:
        p.print_player_status()
    for p in properties:
        p.print_property_status()

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
            play_monopoly(current_player, players, properties)
            if current_player.doubles:
                play_monopoly(current_player, players, properties)
                if current_player.doubles:
                    play_monopoly(current_player, players, properties)
                    if current_player.doubles:
                        play_monopoly(current_player, players, properties)

        print(f"\n--------------- ROUND {round+1} / {max_rounds} END ---------------\n")
        round += 1

def play_monopoly(current_player, players, properties):
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
    display_game_state(players, properties)

    if current_player.jail_turns > 0:
        current_player.jail_turns -= 1
        current_player.jail = False
    if current_player.doubles:
        print(f"{current_player.name} rolled double ({d1}, {d2}), his/her turn again!")
