# from flask import Flask, request, jsonify, json, render_template, flash, redirect, url_for
# app = Flask(__name__)
#
# #http://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates
import os
import sys

from flask import Flask, render_template, request
from Universe import Universe, Player, Item, Market
from random import randint

app = Flask(__name__)
region_name_list = ["Blue light", "Ard", "Shreyu", "North Avenue East",
                    "Florida Man", "Cookout", "Emory", "Bidet",
                    "Braces", "Gorilla"]
universe = Universe(region_name_list, 0, None)
universe_list = universe.__str__()
special_item_key = randint(0, 9)
name = "RITHIK"
engineer = 0
pilot = 0
merchant = 0
fighter = 0
region = Universe.regions[1]
credit = 0
ship = "None"
inventory = {}
player = Player(name, engineer, pilot, merchant, fighter, region, credit, ship, inventory)
wood = Item("Wood", 27, ["AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                         "MODERN", "FUTURISTIC"])
oil = Item("Oil", 16, ["INDUSTRIAL", "MODERN", "FUTURISTIC"])
glass = Item("Glass", 21, ["PRE-AG", "AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                           "MODERN", "FUTURISTIC"])
metal = Item("Metal", 15, ["PRE-AG", "AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                           "MODERN", "FUTURISTIC"])
computer = Item("Computer", 40, ["MODERN", "FUTURISTIC"])
flower = Item("Flower", 32, ["AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "MODERN"])
water = Item("Water", 54, ["PRE-AG", "AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                           "MODERN", "FUTURISTIC"])
phone = Item("Phone", 35, ["MODERN", "FUTURISTIC"])
caviar = Item("Caviar", 45, ["MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                             "MODERN", "FUTURISTIC"])
pineapple = Item("Pineapple", 30, ["AGRICULTURE", "MEDIEVAL", "RENAISSANCE", "INDUSTRIAL",
                                   "MODERN", "FUTURISTIC"])
vibranium = Item("Vibranium", 60, ["MODERN", "FUTURISTIC"])
item_list = [wood, oil, glass, metal, computer, flower, water, phone, caviar,
             pineapple, vibranium]
npc_encounter = False
old_location = ""
flee = False
karma = 0


def reset():
    global region_name_list
    region_name_list = ["Blue light", "Ard", "Shreyu", "North Avenue East",
                        "Florida Man", "Cookout", "Emory", "Bidet",
                        "Braces", "Gorilla"]
    global universe
    universe = Universe(region_name_list, 0, None)
    global universe_list
    universe_list = universe.__str__()
    global special_item_key
    special_item_key = randint(0, 9)
    global engineer
    engineer = 0
    global pilot
    pilot = 0
    global merchant
    merchant = 0
    global fighter
    fighter = 0
    global region
    region = Universe.regions[1]
    global credit
    credit = 0
    global inventory
    inventory = {}
    player.set_engineer(0)
    player.set_pilot(0)
    player.set_merchant(0)
    player.set_fighter(0)
    player.set_fighter(0)
    player.set_region(Universe.regions[1])
    player.set_credit(0)
    player.set_inventory({})
    global npc_encounter
    npc_encounter = False
    global old_location
    old_location = ""
    global flee
    flee = False
    global karma
    karma = 0
    player.get_ship().ship_health = player.get_ship().max_ship_health
    player.get_ship().fuel_capacity = player.get_ship().max_fuel_capacity
    player.get_ship().cargo_space = player.get_ship().max_cargo_space


@app.route("/")
def hello():
    """
    routes to base url/page
    :return: base.html
    """
    reset()
    return render_template("base.html")


@app.route("/login")
def login():
    """
    routes to login page
    :return: login.html
    """
    return render_template("login.html")


@app.route("/display")
def display():
    """
    routes to display page for the player
    :return: display.html
    """
    return render_template("display.html")


@app.route("/loginerror")
def loginerror():
    """
    routes to a login error page
    :return: loginerror.html
    """
    return render_template("loginerror.html")


@app.route("/fuelerror")
def fuelerror():
    """
    routes to a fuel error page
    :return: fuelerror.html
    """
    return render_template("fuelerror.html")


@app.route("/cargoerror")
def cargoerror():
    """
    routes to a fuel error page
    :return: cargoerror.html
    """
    return render_template("cargoerror.html")


@app.route("/crediterror")
def crediterror():
    """
    routes to a fuel error page
    :return: crediterror.html
    """
    return render_template("crediterror.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    """
    routes to a display page or
    routes to a login error function
    :return: display.html
    """
    result = request.form
    name = request.form.get('Name')
    new_engineer = int(request.form.get('Engineer'))
    new_pilot = int(request.form.get('Pilot'))
    new_merchant = int(request.form.get('Merchant'))
    new_fighter = int(request.form.get('Fighter'))
    if request.form.get('Difficulty') == "Easy":
        universe.difficulty = "Easy"
        starting_credits = 1000
        new_max = 16
    elif request.form.get('Difficulty') == "Medium":
        universe.difficulty = "Medium"
        starting_credits = 500
        new_max = 12
    else:
        universe.difficulty = "Hard"
        starting_credits = 100
        new_max = 8
    if new_engineer + new_pilot + new_merchant + new_fighter <= new_max:
        player.set_name(name)
        player.set_engineer(new_engineer)
        player.set_pilot(new_pilot)
        player.set_merchant(new_merchant)
        player.set_fighter(new_fighter)
        player.set_credit(starting_credits)
        ship = player.get_ship()
        starting_fc = ship.max_fuel_capacity
        starting_cs = ship.max_cargo_space
        starting_h = ship.max_ship_health
        return render_template("display.html", result=result, startingCredits=starting_credits,
                               engineer=new_engineer, pilot=new_pilot, merchant=new_merchant,
                               fighter=new_fighter, ship=ship, starting_fc=starting_fc,
                               starting_cs=starting_cs, starting_h=starting_h)
    return loginerror()


@app.route("/universemap")
def universe_map():
    """
    renders the universe map template
    :return: universemap.html
    """
    return render_template("universemap.html", universelist=universe_list)


@app.route('/buy')
def buy():
    item_market = request.args.get('item_market')
    global karma
    karma -= 3
    price_buy_value = int(request.args.get('price_buy_value'))
    if player.get_ship().cargo_space - 1 < 0:
        return cargoerror()
    if player.get_credit() - price_buy_value <= 0:
        return crediterror()
    player.get_ship().cargo_space -= 1
    for item in item_list:
        if item_market == item.name:
            item.set_selling_price(player.get_merchant())
            inventory[item] = item.get_selling_price()
    player.set_inventory(inventory)
    player.set_credit(player.get_credit() - price_buy_value)
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route('/sell')
def sell():
    item_inventory = request.args.get('item_inventory')
    global karma
    karma += 7
    price_sell_value = int(request.args.get('price_sell_value'))
    player.get_ship().cargo_space += 1
    for item in item_list:
        if item_inventory == item.name:
            del inventory[item]
    player.set_inventory(inventory)
    player.set_credit(player.get_credit() + price_sell_value)
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route("/refuel")
def refuel():
    if player.get_credit() < 100:
        return render_template("refuelerror.html")
    else:
        player.set_credit(player.get_credit() - 100)
        player.get_ship().fuel_capacity = player.get_ship().max_fuel_capacity
        if player.get_region().name == "Blue light":
            return blue_light()
        elif player.get_region().name == "Ard":
            return ard()
        elif player.get_region().name == "Shreyu":
            return shreyu()
        elif player.get_region().name == "North Avenue East":
            return north_avenue_east()
        elif player.get_region().name == "Florida Man":
            return florida_man()
        elif player.get_region().name == "Braces":
            return braces()
        elif player.get_region().name == "Cookout":
            return cookout()
        elif player.get_region().name == "Emory":
            return emory()
        elif player.get_region().name == "Bidet":
            return bidet()
        else:
            return gorilla()


@app.route("/refuelerror")
def refuelerror():
    return render_template("refuelerror.html")


@app.route("/repair")
def repair():
    cRepair = (200 * ((16 - player.get_engineer()) / 10.0))
    if player.get_credit() < cRepair:
        return render_template("refuelerror.html")
    else:
        player.set_credit(player.get_credit() - cRepair)
        player.get_ship().ship_health = player.get_ship().max_ship_health
        if player.get_region().name == "Blue light":
            return blue_light()
        elif player.get_region().name == "Ard":
            return ard()
        elif player.get_region().name == "Shreyu":
            return shreyu()
        elif player.get_region().name == "North Avenue East":
            return north_avenue_east()
        elif player.get_region().name == "Florida Man":
            return florida_man()
        elif player.get_region().name == "Braces":
            return braces()
        elif player.get_region().name == "Cookout":
            return cookout()
        elif player.get_region().name == "Emory":
            return emory()
        elif player.get_region().name == "Bidet":
            return bidet()
        else:
            return gorilla()


@app.route("/trader")
def trader():
    return render_template("NPC/trader.html")


@app.route("/trader_buy")
def trader_buy():
    if player.get_ship().cargo_space - 1 < 0:
        return cargoerror()
    if player.get_credit() - 10 < 0:
        return crediterror()
    player.get_ship().cargo_space -= 1
    inventory["Water"] = 10
    player.set_inventory(inventory)
    player.set_credit(player.get_credit() - 10)
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route("/trader_ignore")
def trader_ignore():
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route("/trader_rob")
def trader_rob():
    prob_win = randint(1, 2)
    if player.get_fighter() * prob_win < 16:
        player.get_ship().ship_health -= 10
        return render_template("NPC/roblose.html")
    else:
        if player.get_ship().cargo_space - 1 < 0:
            return cargoerror()
        if player.get_credit() - 10 < 0:
            return crediterror()
        player.get_ship().cargo_space -= 1
        inventory["Water"] = 10
        player.set_inventory(inventory)
        player.set_credit(player.get_credit() - 10)
        return render_template("NPC/robwin.html")


@app.route("/trader_negotiate")
def trader_negotiate():
    prob_win = randint(1, 2)
    if player.get_merchant() * prob_win < 16:
        inventory["Water"] = 13
        return render_template("NPC/negotiatelose.html")
    else:
        if player.get_ship().cargo_space - 1 < 0:
            return cargoerror()
        if player.get_credit() - 10 < 0:
            return crediterror()
        player.get_ship().cargo_space -= 1
        inventory["Water"] = 3
        player.set_inventory(inventory)
        player.set_credit(player.get_credit() - 3)
        return render_template("NPC/negotiatewin.html")


@app.route("/travel_back")
def travel_back():
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route("/bandit")
def bandit():
    return render_template("NPC/bandit.html")


@app.route('/bandit_pay')
def bandit_pay():
    if player.get_credit() - 150 > 0:
        player.set_credit(player.get_credit() - 150)
    elif player.get_inventory() != {}:
        player.set_inventory({})
    else:
        player.get_ship().ship_health -= 15
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route('/bandit_flee')
def bandit_flee():
    global flee
    flee = True
    if player.get_pilot() < 8:
        player.set_credit(0)
        player.get_ship().ship_health -= 15
    if old_location == "Blue light":
        return blue_light()
    elif old_location == "Ard":
        return ard()
    elif old_location == "Shreyu":
        return shreyu()
    elif old_location == "North Avenue East":
        return north_avenue_east()
    elif old_location == "Florida Man":
        return florida_man()
    elif old_location == "Braces":
        return braces()
    elif old_location == "Cookout":
        return cookout()
    elif old_location == "Emory":
        return emory()
    elif old_location == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route('/bandit_fight')
def bandit_fight():
    if player.get_fighter() > 8:
        player.set_credit(player.get_credit() + 150)
    else:
        player.set_credit(0)
        player.get_ship().ship_health -= 15
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route("/police")
def police():
    makelist = player.get_inventory()
    makelist = list(makelist.keys())
    return render_template("NPC/police.html", stolen_item=makelist[0].name)


@app.route('/police_forfeit')
def police_forfeit():
    del inventory[list(player.get_inventory().keys())[0]]
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route('/police_flee')
def police_flee():
    global flee
    flee = True
    if player.get_pilot() < 8:
        del inventory[list(player.get_inventory().keys())[0]]
        player.set_credit(player.get_credit() - 150)
        player.get_ship().ship_health -= 15
    if old_location == "Blue light":
        return blue_light()
    elif old_location == "Ard":
        return ard()
    elif old_location == "Shreyu":
        return shreyu()
    elif old_location == "North Avenue East":
        return north_avenue_east()
    elif old_location == "Florida Man":
        return florida_man()
    elif old_location == "Braces":
        return braces()
    elif old_location == "Cookout":
        return cookout()
    elif old_location == "Emory":
        return emory()
    elif old_location == "Bidet":
        return bidet()
    else:
        return gorilla()


@app.route('/police_fight')
def police_fight():
    if player.get_fighter() < 8:
        del inventory[list(player.get_inventory().keys())[0]]
    if player.get_region().name == "Blue light":
        return blue_light()
    elif player.get_region().name == "Ard":
        return ard()
    elif player.get_region().name == "Shreyu":
        return shreyu()
    elif player.get_region().name == "North Avenue East":
        return north_avenue_east()
    elif player.get_region().name == "Florida Man":
        return florida_man()
    elif player.get_region().name == "Braces":
        return braces()
    elif player.get_region().name == "Cookout":
        return cookout()
    elif player.get_region().name == "Emory":
        return emory()
    elif player.get_region().name == "Bidet":
        return bidet()
    else:
        return gorilla()


def npc():
    universe.times_traveled = 0
    choose_npc = randint(1, 10)
    if karma <= 0:
        if universe.difficulty == "Easy":
            if 1 <= choose_npc <= 6:
                return trader()
            elif 7 <= choose_npc <= 8:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 9 <= choose_npc <= 10:
                return bandit()
        if universe.difficulty == "Medium":
            if 1 <= choose_npc <= 4:
                return trader()
            elif 5 <= choose_npc <= 7:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 8 <= choose_npc <= 10:
                return bandit()
        if universe.difficulty == "Hard":
            if 1 <= choose_npc <= 2:
                return trader()
            elif 3 <= choose_npc <= 6:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 7 <= choose_npc <= 10:
                return bandit()
    else:
        if universe.difficulty == "Easy":
            if 1 <= choose_npc <= 7:
                return trader()
            elif 8 <= choose_npc <= 9:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 9 <= choose_npc <= 10:
                return bandit()
        if universe.difficulty == "Medium":
            if 1 <= choose_npc <= 6:
                return trader()
            elif 7 <= choose_npc <= 8:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 9 <= choose_npc <= 10:
                return bandit()
        if universe.difficulty == "Hard":
            if 1 <= choose_npc <= 5:
                return trader()
            elif 6 <= choose_npc <= 7:
                if player.get_inventory() == {}:
                    return bandit()
                else:
                    return police()
            elif 7 <= choose_npc <= 10:
                return bandit()


@app.route("/special")
def special():
    if player.get_credit() - 100 >= 0:
        return render_template("specialgameover.html", name=player.get_name())
    else:
        return render_template("crediterror.html")


@app.route("/Blue light")
def blue_light():
    """
    routes to the blue light region
    :return: regions/blueLight.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[0])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[0], player)
    cargo_space = player.get_ship().cargo_space
    blue_light_market = Market("Blue Light Market", {})
    blue_light_market.set_market(item_list, universe_list[0][3][12:])
    for item in blue_light_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[0][0][8:])
        blue_light_market.market[item] = item.get_buying_price()
    return render_template("Regions/blueLight.html", xcoord=universe_list[0][1],
                           ycoord=universe_list[0][2], techlevel=universe_list[0][3],
                           fuelcost=fuel_costs, market=blue_light_market.market,
                           total_fc=total_fc, cargo_space=cargo_space,
                           inventory=player.get_inventory(), credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Ard")
def ard():
    """
    routes to the ard region
    :return: regions/ard.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[1])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[1], player)
    ard_market = Market("Ard Market", {})
    ard_market.set_market(item_list, universe_list[1][3][12:])
    cargo_space = player.get_ship().cargo_space
    for item in ard_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[1][0][8:])
        ard_market.market[item] = item.get_buying_price()
    return render_template("Regions/Ard.html", xcoord=universe_list[1][1],
                           ycoord=universe_list[1][2], techlevel=universe_list[1][3],
                           fuelcost=fuel_costs, market=ard_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(), cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Shreyu")
def shreyu():
    """
    routes to the Shreyu region
    return: regions/Shreyu.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[2])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[2], player)
    cargo_space = player.get_ship().cargo_space
    shreyu_market = Market("Shreyu Market", {})
    shreyu_market.set_market(item_list, universe_list[2][3][12:])
    for item in shreyu_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[2][0][8:])
        shreyu_market.market[item] = item.get_buying_price()
    return render_template("Regions/Shreyu.html", xcoord=universe_list[2][1],
                           ycoord=universe_list[2][2], techlevel=universe_list[2][3],
                           fuelcost=fuel_costs, market=shreyu_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(), cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/North Avenue East")
def north_avenue_east():
    """
    routes to the north avenue east region
    :return: regions/northAvenueEast.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[3])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[3], player)
    cargo_space = player.get_ship().cargo_space
    north_avenue_east_market = Market("North Avenue East Market", {})
    north_avenue_east_market.set_market(item_list, universe_list[3][3][12:])
    for item in north_avenue_east_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[3][0][8:])
        north_avenue_east_market.market[item] = item.get_buying_price()
    return render_template("Regions/northAvenueEast.html", xcoord=universe_list[3][1],
                           ycoord=universe_list[3][2], techlevel=universe_list[3][3],
                           fuelcost=fuel_costs, market=north_avenue_east_market.market,
                           total_fc=total_fc, cargo_space=cargo_space,
                           inventory=player.get_inventory(), credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Florida Man")
def florida_man():
    """
    routes to the florida man region
    :return: regions/floridaMan.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[4])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[4], player)
    cargo_space = player.get_ship().cargo_space
    florida_man_market = Market("Florida Man Market", {})
    florida_man_market.set_market(item_list, universe_list[4][3][12:])
    for item in florida_man_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[4][0][8:])
        florida_man_market.market[item] = item.get_buying_price()
    return render_template("Regions/floridaMan.html", xcoord=universe_list[4][1],
                           ycoord=universe_list[4][2], techlevel=universe_list[4][3],
                           fuelcost=fuel_costs, market=florida_man_market.market,
                           total_fc=total_fc, cargo_space=cargo_space,
                           inventory=player.get_inventory(), credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Cookout")
def cookout():
    """
    routes to the cookout region
    :return: regions/cookout.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[5])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[5], player)
    cargo_space = player.get_ship().cargo_space
    cookout_market = Market("Cookout Market", {})
    cookout_market.set_market(item_list, universe_list[5][3][12:])
    for item in cookout_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[5][0][8:])
        cookout_market.market[item] = item.get_buying_price()
    return render_template("Regions/cookout.html", xcoord=universe_list[5][1],
                           ycoord=universe_list[5][2], techlevel=universe_list[5][3],
                           fuelcost=fuel_costs, market=cookout_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Emory")
def emory():
    """
    routes to the emory region
    :return: regions/emory.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[6])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[6], player)
    cargo_space = player.get_ship().cargo_space
    emory_market = Market("Emory Market", {})
    emory_market.set_market(item_list, universe_list[6][3][12:])
    for item in emory_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[6][0][8:])
        emory_market.market[item] = item.get_buying_price()
    return render_template("Regions/emory.html", xcoord=universe_list[6][1],
                           ycoord=universe_list[6][2], techlevel=universe_list[6][3],
                           fuelcost=fuel_costs, market=emory_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Bidet")
def bidet():
    """
    routes to the bidet region
    :return: regions/bidet.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[7])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[7], player)
    bidet_market = Market("Bidet Market", {})
    bidet_market.set_market(item_list, universe_list[7][3][12:])
    cargo_space = player.get_ship().cargo_space
    for item in bidet_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[7][0][8:])
        bidet_market.market[item] = item.get_buying_price()
    return render_template("Regions/bidet.html", xcoord=universe_list[7][1],
                           ycoord=universe_list[7][2], techlevel=universe_list[7][3],
                           fuelcost=fuel_costs, market=bidet_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Braces")
def braces():
    """
    routes to the braces region
    :return: regions/braces.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[8])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[8], player)
    cargo_space = player.get_ship().cargo_space
    braces_market = Market("Braces Market", {})
    braces_market.set_market(item_list, universe_list[8][3][12:])
    for item in braces_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[8][0][8:])
        braces_market.market[item] = item.get_buying_price()
    return render_template("Regions/braces.html", xcoord=universe_list[8][1],
                           ycoord=universe_list[8][2], techlevel=universe_list[8][3],
                           fuelcost=fuel_costs, market=braces_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


@app.route("/Gorilla")
def gorilla():
    """
    routes to the gorilla region
    :return: regions/gorilla.html
    """
    global npc_encounter
    global old_location
    global flee
    if request.args.get('fc_sub') is None:
        fc_sub = 0
    else:
        fc_sub = request.args.get('fc_sub')
    total_fc = player.get_ship().fuel_capacity
    old_location = player.get_region().name
    player.set_region(Universe.regions[9])
    # npc encounter
    if player.get_ship().ship_health <= 0:
        return render_template("gameover.html")
    if not flee:
        if not npc_encounter:
            if total_fc - int(fc_sub) < 0:
                return render_template("fuelerror.html")
            total_fc = total_fc - int(fc_sub)
            player.get_ship().fuel_capacity = total_fc
            universe.times_traveled += 1
            if universe.difficulty == "Easy":
                if universe.times_traveled == 8:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Medium":
                if universe.times_traveled == 5:
                    npc_encounter = True
                    return npc()
            if universe.difficulty == "Hard":
                if universe.times_traveled == 3:
                    npc_encounter = True
                    return npc()
        else:
            npc_encounter = False
    flee = False
    fuel_costs = universe.get_fuel_costs(Universe.regions[9], player)
    cargo_space = player.get_ship().cargo_space
    gorilla_market = Market("Gorilla Market", {})
    gorilla_market.set_market(item_list, universe_list[9][3][12:])
    for item in gorilla_market.market:
        item.set_buying_price(player.get_merchant(), universe_list[9][0][8:])
        gorilla_market.market[item] = item.get_buying_price()
    return render_template("Regions/gorilla.html", xcoord=universe_list[9][1],
                           ycoord=universe_list[9][2], techlevel=universe_list[9][3],
                           fuelcost=fuel_costs, market=gorilla_market.market, total_fc=total_fc,
                           cargo_space=cargo_space, inventory=player.get_inventory(),
                           credits=player.get_credit(),
                           cRepair=(200 * ((16 - player.get_engineer()) / 10.0)),
                           shealth=player.get_ship().ship_health, special_item_key=special_item_key,
                           karma=karma, name=player.get_name())


if __name__ == '__main__':
    app.run(debug=True)
