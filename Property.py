class Property:                                                     # Cities and places
    def __init__(self, name, type, country, price, rent, index):
        self.name = name
        self.country = country
        self.type = type
        self.price = price
        self.rent = rent
        self.index = index
        self.owner = None

    def upgrade(self, name, type, country, cur_price, cur_rent):    # Build Hotels and Apartments
        if self.country in self.owner.countries:
            self.price = 0.5 * cur_price
            self.rent = cur_rent * 1.5

    def print_property_status(self):
        print(f"| ________________{(self.index)}__________________")
        print(f"| {self.name} is {self.type}")
        print(f"| {self.name} is in {self.country}")
        print(f"| {self.name} has ${self.price} price")
        print(f"| {self.name} has ${self.rent} rent")
        print(f"| {self.name} owner is {(self.owner).__repr__()}")

    def __str__(self):
        return ("\n" + "TYPE: " + str(type(self).__name__) + 
                "\n" + "Name: " + str(self.name) + 
                "\n" + "Country: " + str(self.country) + 
                "\n" + "Type: " + str(self.type) + 
                "\n" + "Price: " + str(self.price) + 
                "\n" + "Rent: " + str(self.rent) + 
                "\n" + "Owner: " + str(self.owner) + 
                "\n")

    def __repr__(self):
        if self.owner:
            return (str(self.name) + ": " + str(self.price) + ": " + str(self.rent))
        else:
            return (str(self.name) + ": " + str(self.price) + ": " + str(self.rent))

#TODO_: complete this
'''
def auction(player1, player2):
    # Check if both players agree to exchange the cities
    if players[0].agree_to_exchange(cities) and players[1].agree_to_exchange(cities):
        
        # Exchange the ownership of the cities
        players[0].remove_city(cities[0])
        players[1].add_city(cities[0])
        players[1].remove_city(cities[1])
        players[0].add_city(cities[1])
        
        print("The cities were exchanged between the players.")
        
    else:
        print("The players did not agree to exchange the cities.")
'''
