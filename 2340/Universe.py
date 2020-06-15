from random import randint


class Region:
    name = ""
    tech_level = ""

    def __init__(self, x_coord, y_coord, name, tech_level):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.name = name
        self.tech_level = tech_level



class Game:
    # accessibility in region class?
    region_name_list = ["Blue light", "Ard", "Shreyu", "North Avenue East", "Florida Man",
                        "Cookout", "Emory", "Bidet", "Braces", "Gorilla"]

    def __init__(self, difficulty):
        self.difficulty = difficulty


class Universe:
    tech_level_list = ["PRE-AG", "AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                       "MODERN", "FUTURISTIC"]
    region_name_list = ["Blue light", "Ard", "Shreyu", "North Avenue East", "Florida Man",
                        "Cookout", "Emory", "Bidet", "Braces", "Gorilla"]
    regions = []

    def __init__(self, regions, times_traveled, difficulty):
        self.regions = Universe.regions
        self.times_traveled = times_traveled
        self.difficulty = difficulty
        self.tech_level_list = Universe.tech_level_list
        self.make_regions(regions, self.tech_level_list)
        self.regions = Universe.regions

    def make_regions(self, region_name_list, tech_level_list):
        for i in range(10):
            region_name = region_name_list[i]
            tech_level = tech_level_list[randint(0, 6)]
            num_valid_y = 0
            num_valid_x = 0
            x_coord = randint(-200, 200)
            y_coord = randint(-200, 200)
            region = Region(x_coord, y_coord, region_name, tech_level)
            region.tech_level = tech_level
            region.region_name = region_name
            if len(self.regions) == 0:
                region.x_coord = x_coord
                region.y_coord = y_coord
                self.regions.append(region)
            else:
                valid_y = False
                while not valid_y:
                    y_coord = randint(-200, 200)
                    for element in self.regions:
                        if abs(y_coord - element.y_coord) > 5:
                            num_valid_y += 1
                        if num_valid_y == len(self.regions):
                            valid_y = True
                valid_x = False
                while not valid_x:
                    x_coord = randint(-200, 200)
                    for element in self.regions:
                        if abs(x_coord - element.x_coord) > 5:
                            num_valid_x += 1
                        if num_valid_x == len(self.regions):
                            valid_x = True
                region.x_coord = x_coord
                region.y_coord = y_coord
                self.regions.append(region)

    def get_fuel_costs(self, current, player):
        region_array = self.regions

        fuel_costs = []
        for element in region_array:
            if element == current:
                continue
            fuel_costs.append(self.fuel_cost_helper(element, player))
        return fuel_costs

    def fuel_cost_helper(self, element, player):
        x_1 = player.get_region().x_coord
        y_1 = player.get_region().y_coord
        x_2 = element.x_coord
        y_2 = element.y_coord
        distance = ((x_2 - x_1)**2 + (y_2 - y_1)**2)**(0.5)
        pskill = (17 - player.get_pilot())/10
        fcost = distance*pskill
        return int(fcost)

    def __str__(self):
        overall_array = []
        for i in self.regions:
            region_array = ["Region: " + i.name, "X-Coordinate: " + str(i.x_coord),
                            "Y-Coordinate: " + str(i.y_coord), "Tech Level: " + str(i.tech_level)]
            overall_array.append(region_array)
        return overall_array


class Player:
    #max_cargo_space, max_fuel_capacity, max_ship_health
    ship_name_dict = {"Saisamhitha Mahabaleshwarkar": [7, 5000, 100],
                      "Hurricane": [6, 4000, 90],
                      "Raj": [5, 3000, 70],
                      "Rambler": [4, 2500, 60],
                      "Shipt": [3, 2000, 50]}
    ship_list = []

    def __init__(self, name, engineer, pilot, merchant, fighter, region, credit, ship, inventory):
        # assign int attributes
        self.__name = name
        self.__engineer = engineer
        self.__pilot = pilot
        self.__merchant = merchant
        self.__fighter = fighter
        self.__region = region
        self.__credit = credit
        self.__ship = ship
        self.ship_list = Player.ship_list
        self.ship_name_dict = Player.ship_name_dict
        self.create_ship(self.ship_list, self.ship_name_dict)
        self.__ship = Player.ship_list[0]
        self.__inventory = inventory



    def create_ship(self, ship_list, ship_name_dict):
        keys = list(ship_name_dict.keys())
        key2 = randint(0, 4)
        use_key = keys[key2]
        cargo_space = ship_name_dict[use_key][0]
        fuel_capacity = ship_name_dict[use_key][1]
        ship_health = ship_name_dict[use_key][2]
        ship_obj = Ship(use_key, cargo_space, fuel_capacity, ship_health)
        ship_list.append(ship_obj)


    def get_engineer(self):
        return self.__engineer

    def set_engineer(self, engineer):
        self.__engineer = engineer

    def get_pilot(self):
        return self.__pilot

    def set_pilot(self, pilot):
        self.__pilot = pilot

    def get_fighter(self):
        return self.__fighter

    def set_fighter(self, fighter):
        self.__fighter = fighter

    def get_merchant(self):
        return self.__merchant

    def set_merchant(self, merchant):
        self.__merchant = merchant

    def get_region(self):
        return self.__region

    def set_region(self, region):
        self.__region = region

    def get_credit(self):
        return self.__credit

    def set_credit(self, credit):
        self.__credit = credit

    def get_ship(self):
        return self.__ship

    def set_ship(self, ship):
        self.__ship = ship

    def get_inventory(self):
        return self.__inventory


    def set_inventory(self, inventory):
        self.__inventory = inventory;

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name;

    def __str__(self):
        player_array = ["---------------------", "Engineer: " + str(self.get_engineer()),
                        "Pilot: " + str(self.get_pilot()), "Fighter: " + str(self.get_fighter()),
                        "Merchant: " + str(self.get_merchant()),
                        "Region: " + str(self.get_region()), "Credit: " + str(self.get_credit())]
        return player_array

class Ship:
    def __init__(self, type, max_cargo_space, max_fuel_capacity, max_ship_health):
        self.type = type
        self.max_cargo_space = max_cargo_space
        self.max_fuel_capacity = max_fuel_capacity
        self.max_ship_health = max_ship_health
        self.cargo_space = max_cargo_space
        self.fuel_capacity = max_fuel_capacity
        self.ship_health = max_ship_health

    def __str__(self):
        return self.type

class Item:
    def __init__(self, name, base_price, tech_level_list):
        self.name = name
        self.base_price = base_price
        self.buying_price = 0
        self.selling_price = 0
        self.tech_level_list = tech_level_list

    def set_buying_price(self, merchant_skill, region_name):
        self.buying_price = self.base_price
        if merchant_skill < 6:
            self.buying_price = self.buying_price - 2
        elif 12 > merchant_skill >= 6:
            self.buying_price = self.buying_price + 3
        elif merchant_skill >= 12:
            self.buying_price = self.buying_price + 5
        if region_name == "Blue light":
            self.buying_price = self.buying_price + 3
        elif region_name == "Ard":
            self.buying_price -= 5
        elif region_name == "Shreyu":
            self.buying_price += 11
        elif region_name == "North Avenue East":
            self.buying_price -= 2
        elif region_name == "Florida Man":
            self.buying_price += 5
        elif region_name == "Cookout":
            self.buying_price += 18
        elif region_name == "Emory":
            self.buying_price += 12
        elif region_name == "Bidet":
            self.buying_price -= 10
        elif region_name == "Braces":
            self.buying_price += 2
        elif region_name == "Gorilla":
            self.buying_price += 32

    def get_buying_price(self):
        return self.buying_price

    def set_selling_price(self, merchant_skill):
        if(merchant_skill == 0):
            factor = .05
            self.selling_price = int(self.base_price * factor)
        else:
            factor = merchant_skill/16
            self.selling_price = int(self.base_price * factor)

    def get_selling_price(self):
        return self.selling_price

    def __str__(self):
        return self.name

class Market:
    def __init__(self, name, market):
        self.name = name
        self.market = market

    def set_market(self, item_list, region_tech_level):
        for item in item_list:
            for levels in item.tech_level_list:
                if levels == region_tech_level:
                    self.market[item] = item.buying_price