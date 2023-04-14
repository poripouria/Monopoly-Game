"""
Description: Class for defining game board properties
"""

class Property:             # Cities and Places
    def __init__(self, name, type, country, price, rent, index):
        self.name = name
        self.country = country
        self.type = type
        self.price = price
        self.sell_ratio = 0.8
        self.rent = rent
        self.index = index
        self.owner = None
        self.is_upgrade = False
        self.upgrade_level = 0

    def upgrade(self):      # Build Hotels and Apartments
        self.owner.money -= 0.5 * self.price
        self.price *= 1.5
        self.rent *= 1.5
        self.is_upgrade = True
        self.upgrade_level += 1
        self.owner.wealth = self.owner.money + self.owner.properties_value

    def buy(self, player, properties):
        player.properties.append(self)
        player.properties_value += self.price
        player.money -= self.price
        self.owner = player
        if self.type == "city":
            for i in range(40):
                if properties[i].type == "city" and properties[i].country == self.country:
                    if properties[i].owner != player or properties[i].owner is None:
                        break
            else:
                player.countries.append(self.country)
                print(f"{player.name} got all the cities in {self.country}!")
        elif self.type == "service_centers":
            for i in range(40):
                if properties[i].type == "service_centers":
                    if properties[i].owner != player or properties[i].owner is None:
                        break
            else:
                player.countries.append("service_centers")
                print(f"{player.name} got all service centers!")
        player.wealth = player.money + player.properties_value

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
            return (str(self.name) + ": " + str(self.price))
        else:
            return (str(self.name) + ": " + str(self.price))
