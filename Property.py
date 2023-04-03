class Property:             # Cities and Places
    def __init__(self, name, type, country, price, rent, index):
        self.name = name
        self.country = country
        self.type = type
        self.price = price
        self.rent = rent
        self.index = index
        self.owner = None
        self.is_upgrade = False

    def upgrade(self):      # Build Hotels and Apartments
        self.owner.money -= 0.5 * self.price
        self.is_upgrade = True
        self.price *= 1.5
        self.rent *= 1.5

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
