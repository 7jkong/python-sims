import random
import time
import math
import sys

# --- GAME STATE (FIXED: Separate Kitchen Gear) ---
player = {
    "money": 300, # Increased starting money
    "xp": 0,
    "level": 1,
    "stamina": 100,
    "max_stamina": 100,
    "day": 1,
    "hunting_gear": "Basic Knife",
    "cooking_gear": "Old Stove", # NEW: Tracks main cooking gear
    "drink_gear": "None", # NEW: Tracks drink gear
}

# --- INVENTORIES ---
inventory = {
    # Basic
    "rabbit_meat": 0, "berries": 0, "mushrooms": 0, "wild_herbs": 0,
    # Mid-Tier
    "boar_meat": 0, "potatoes": 0, "truffles": 0,
    # High-Tier
    "deer_meat": 0, "rare_herbs": 0, "red_peppers": 0,
    # Exotic/End Game
    "swamp_eel": 0, "exotic_fruit": 0, "mammoth_meat": 0, "crystal_salt": 0, "limes": 0, "frozen_beans": 0,
    # Placeholder for new tiers (4-10 Star)
    "volcanic_egg": 0, "cloud_berries": 0, "abyssal_kelp": 0, "nebula_spice": 0, "glacial_prawn": 0,
    "sun_peaches": 0, "phoenix_ash": 0, "dragon_scale": 0, "star_fruit": 0,

    # Purchased Goods
    "flour": 0, "sugar": 0, "salt": 0, "oil": 0,
    "coffee_beans": 0, "tea_leaves": 0,
}

cooked_meals = {}
# Player starts by knowing 1-star recipes + 1 drink
known_recipes = {"roast_rabbit", "mushroom_stew", "berry_pudding", "berry_tea"}

# --- NEW ORDER SYSTEM ---
active_orders = []

# --- NEW CUSTOMER DIALOGUE DATA (UPDATED WITH DYNAMIC PENALTIES) ---
customer_data = {
    "noble": {
        "name": "The Noble",
        "dialogue": [
            "I require this meal immediately. I simply cannot be seen eating 'Poor' quality.",
            "If this dish is less than 'Good', you will receive a scolding, not a reward!",
            "Chop chop! My banquet waits for no one, peasant chef."
        ],
        # High money loss as penalty, reflects high-society consequences
        "fail_penalty": {"type": "money", "amount": 0.25} # 25% of current money
    },
    "merchant": {
        "name": "The Grumpy Merchant",
        "dialogue": [
            "Just cook the meal. I don't care how, just make sure I get the portion size I asked for.",
            "I'm paying a premium price; don't waste my time with failure.",
            "It better be worth the coin. My time is money."
        ],
        # Fixed money loss, reflects loss of small business revenue
        "fail_penalty": {"type": "money_fixed", "amount": 50}
    },
    "guard": {
        "name": "The Hungry Guard",
        "dialogue": [
            "I'm starved! Make sure the portions are large and the quality is at least 'Good'.",
            "I can't patrol on an empty stomach. Bring the food quickly!",
            "I'll pay extra if it's hot. Don't make me wait."
        ],
        # High XP loss, reflects lack of progress due to inefficiency
        "fail_penalty": {"type": "xp", "amount": 50}
    },
    "chef": {
        "name": "The Royal Chef (who can't cook for himself)",
        "dialogue": [
            "This recipe is for my personal analysis. If you do not do this, you will be punished.",
            "I will be judging your technique. Do not disgrace the culinary arts.",
            "If you fail, I will be forced to buy your ingredients at half price as compensation."
        ],
        # Stamina loss, temporary but painful, reflects exhaustion from scrutiny
        "fail_penalty": {"type": "max_stamina_temp", "amount": 15}
    },
        "jerome": {
        "name": "The Jerome",
        "dialogue": [
            "Hi, gimme all ur money please.",
            "If you don't get a poor for me thanks.",
            "I love poor food so cook me one please."
        ],
        # A joke penalty, flat large money loss
        "fail_penalty": {"type": "money_fixed", "amount": 100}
    },
}
# --- END NEW CUSTOMER DATA ---


# --- GAME DATA (RECIPES, LOCATIONS, UPGRADES) ---

# --- RECIPES (EXPANDED TO 10 STAR) ---
recipes = {
    # 1-STAR RECIPES (Requires "Old Stove" or "Kettle")
    "roast_rabbit": {
        "name": "Roast Rabbit", "ingredients": {"rabbit_meat": 1, "wild_herbs": 1, "salt": 1},
        "base_value": 75, "xp": 15, "star": 1, "stamina_cost": 8
    },
    "mushroom_stew": {
        "name": "Mushroom Stew", "ingredients": {"mushrooms": 3, "potatoes": 1, "oil": 1},
        "base_value": 80, "xp": 18, "star": 1, "stamina_cost": 8
    },
    "berry_pudding": {
        "name": "Berry Pudding", "ingredients": {"berries": 3, "flour": 1, "sugar": 1},
        "base_value": 60, "xp": 12, "star": 1, "stamina_cost": 5
    },
    "berry_tea": {
        "name": "Refreshing Berry Tea", "ingredients": {"tea_leaves": 1, "berries": 2, "sugar": 1},
        "base_value": 50, "xp": 10, "star": 1, "stamina_cost": 4, "type": "drink"
    },
    "simple_coffee": {
        "name": "Simple Brewed Coffee", "ingredients": {"coffee_beans": 2, "sugar": 1},
        "base_value": 60, "xp": 12, "star": 1, "stamina_cost": 5, "type": "drink"
    },


    # 2-STAR RECIPES (Requires "Iron Stove" or "Industrial Brewer")
    "boar_roast": {
        "name": "Boar Roast", "ingredients": {"boar_meat": 1, "potatoes": 2, "wild_herbs": 2, "oil": 1},
        "base_value": 150, "xp": 40, "star": 2, "stamina_cost": 12
    },
    "truffle_pasta": {
        "name": "Truffle Pasta", "ingredients": {"truffles": 1, "flour": 1, "salt": 1, "oil": 1},
        "base_value": 180, "xp": 50, "star": 2, "stamina_cost": 15
    },
    "spicy_sausage": {
        "name": "Spicy Sausage", "ingredients": {"boar_meat": 1, "red_peppers": 1, "salt": 1},
        "base_value": 170, "xp": 45, "star": 2, "stamina_cost": 12
    },
    "energizing_latte": {
        "name": "Energizing Latte", "ingredients": {"coffee_beans": 2, "sugar": 1, "oil": 1},
        "base_value": 130, "xp": 35, "star": 2, "stamina_cost": 10, "type": "drink"
    },

    # 3-STAR RECIPES (Requires "Chef's Oven" or "Industrial Brewer")
    "venison_steak": {
        "name": "Venison Steak", "ingredients": {"deer_meat": 1, "rare_herbs": 1, "oil": 1, "potatoes": 1},
        "base_value": 360, "xp": 110, "star": 3, "stamina_cost": 25
    },
    "eel_curry": {
        "name": "Exotic Eel Curry", "ingredients": {"swamp_eel": 1, "exotic_fruit": 2, "rare_herbs": 1, "red_peppers": 1},
        "base_value": 640, "xp": 200, "star": 3, "stamina_cost": 30
    },
    "mammoth_tenderloin": {
        "name": "Mammoth Tenderloin", "ingredients": {"mammoth_meat": 1, "crystal_salt": 1, "oil": 1, "frozen_beans": 1},
        "base_value": 1100, "xp": 350, "star": 3, "stamina_cost": 35
    },
    "lunar_lime_pie": {
        "name": "Lunar Lime Pie", "ingredients": {"limes": 2, "sugar": 1, "flour": 1, "exotic_fruit": 1},
        "base_value": 600, "xp": 180, "star": 3, "stamina_cost": 28
    },
    "hearty_venison_chili": {
        "name": "Hearty Venison Chili", "ingredients": {"deer_meat": 1, "red_peppers": 2, "potatoes": 2, "rare_herbs": 1},
        "base_value": 500, "xp": 150, "star": 3, "stamina_cost": 25
    },
    "elixir_of_life": {
        "name": "Elixir of Life", "ingredients": {"rare_herbs": 2, "crystal_salt": 1, "limes": 1, "exotic_fruit": 1},
        "base_value": 750, "xp": 250, "star": 3, "stamina_cost": 20, "type": "drink"
    },
   
    # 4-STAR RECIPES (Requires "Industrial Oven" or "Advanced Brewer")
    "volcanic_stew": {
        "name": "Volcanic Egg Stew", "ingredients": {"volcanic_egg": 1, "red_peppers": 3, "salt": 1, "oil": 1},
        "base_value": 1500, "xp": 500, "star": 4, "stamina_cost": 45
    },
    "cloudberry_tart": {
        "name": "Cloudberry Tart", "ingredients": {"cloud_berries": 2, "sugar": 2, "flour": 1, "crystal_salt": 1},
        "base_value": 1300, "xp": 450, "star": 4, "stamina_cost": 40
    },
    "seaweed_wrap": {
        "name": "Abyssal Kelp Wrap", "ingredients": {"abyssal_kelp": 2, "swamp_eel": 1, "rare_herbs": 1, "limes": 1},
        "base_value": 1700, "xp": 550, "star": 4, "stamina_cost": 50
    },
    "nebula_tea": {
        "name": "Nebula Spice Tea", "ingredients": {"nebula_spice": 1, "tea_leaves": 2, "sugar": 1, "limes": 1},
        "base_value": 1200, "xp": 400, "star": 4, "stamina_cost": 30, "type": "drink"
    },

    # 5-STAR RECIPES (Requires "Fusion Cooker" or "Advanced Brewer")
    "prawn_cocktail": {
        "name": "Glacial Prawn Cocktail", "ingredients": {"glacial_prawn": 1, "limes": 2, "rare_herbs": 1, "exotic_fruit": 1},
        "base_value": 2500, "xp": 800, "star": 5, "stamina_cost": 60
    },
    "sun_peach_sorbet": {
        "name": "Sun Peach Sorbet", "ingredients": {"sun_peaches": 2, "sugar": 2, "flour": 1, "crystal_salt": 1},
        "base_value": 2200, "xp": 700, "star": 5, "stamina_cost": 55
    },
    "phoenix_broth": {
        "name": "Phoenix Ash Broth", "ingredients": {"phoenix_ash": 1, "rare_herbs": 2, "oil": 1, "salt": 1},
        "base_value": 3000, "xp": 1000, "star": 5, "stamina_cost": 70
    },
   
    # 6-STAR RECIPES (Requires "Fusion Cooker" or "Master Brewer")
    "dragon_scale_soup": {
        "name": "Dragon Scale Soup", "ingredients": {"dragon_scale": 1, "volcanic_egg": 1, "nebula_spice": 1, "abyssal_kelp": 1},
        "base_value": 4500, "xp": 1500, "star": 6, "stamina_cost": 80
    },
    "star_fruit_jelly": {
        "name": "Star Fruit Jelly", "ingredients": {"star_fruit": 2, "sugar": 3, "flour": 1, "cloud_berries": 1},
        "base_value": 4000, "xp": 1200, "star": 6, "stamina_cost": 75
    },
   
    # Placeholder recipes for 7-10 stars (Requires "Aether Oven" or "Master Brewer")
    # For a full game, more locations/ingredients/gear would be needed for these.
    "tier7_dish": {
        "name": "Cosmic Ragu", "ingredients": {"nebula_spice": 2, "volcanic_egg": 1, "mammoth_meat": 1},
        "base_value": 6000, "xp": 2000, "star": 7, "stamina_cost": 90
    },
    "tier8_dish": {
        "name": "Planetary Pie", "ingredients": {"star_fruit": 2, "sun_peaches": 2, "flour": 2, "sugar": 2},
        "base_value": 8000, "xp": 3000, "star": 8, "stamina_cost": 100
    },
    "tier9_dish": {
        "name": "Divine Nectar", "ingredients": {"phoenix_ash": 1, "dragon_scale": 1, "limes": 1, "exotic_fruit": 1},
        "base_value": 10000, "xp": 4000, "star": 9, "stamina_cost": 120, "type": "drink"
    },
    "tier10_dish": {
        "name": "Ultimate Feast", "ingredients": {"dragon_scale": 2, "phoenix_ash": 2, "glacial_prawn": 1, "nebula_spice": 1},
        "base_value": 15000, "xp": 6000, "star": 10, "stamina_cost": 150
    },
}

# --- HUNT LOCATIONS (EXPANDED) ---
hunt_locations = {
    "forest": {
        "name": "Forest", "gear_req": "Basic Knife", "level_req": 1, "stamina_cost": 15,
        "loot": [("rabbit_meat", 3, 0.9), ("berries", 5, 0.9), ("mushrooms", 4, 0.8), ("wild_herbs", 3, 0.6)],
        "messages": ["You tracked a small rabbit through the undergrowth.", "You found a patch of fresh berries.", "You spotted some edible mushrooms near a damp log.", "You gathered some fragrant wild herbs."]
    },
    "plains": {
        "name": "Plains", "gear_req": "Sturdy Axe", "level_req": 3, "stamina_cost": 25,
        "loot": [("boar_meat", 3, 0.6), ("wild_herbs", 5, 0.9), ("potatoes", 4, 0.7), ("truffles", 2, 0.4)],
        "messages": ["You narrowly avoided the tusks of a wild boar!", "You gathered some fragrant wild herbs.", "You dug up a few wild potatoes.", "You smelled and dug up a rare truffle!"]
    },
    "mountains": {
        "name": "Mountains", "gear_req": "Hunting Rifle", "level_req": 7, "stamina_cost": 40,
        "loot": [("deer_meat", 3, 0.5), ("rare_herbs", 3, 0.6), ("red_peppers", 2, 0.5)],
        "messages": ["A clean shot brings down a prized deer.", "You scaled a small cliff to find some rare herbs.", "You found a small cluster of fiery red peppers."]
    },
    "swamp": {
        "name": "Swamp", "gear_req": "Hunting Rifle", "level_req": 10, "stamina_cost": 50,
        "loot": [("swamp_eel", 2, 0.6), ("exotic_fruit", 4, 0.7), ("rare_herbs", 2, 0.4), ("limes", 3, 0.6)],
        "messages": ["You wrestled a slimy swamp eel from the mud.", "You found a rare, bright-colored fruit hanging over the water.", "The heat makes hunting difficult, but rewarding.", "You picked some tangy swamp limes."]
    },
    "ice_peaks": {
        "name": "Ice Peaks", "gear_req": "Ice Pick Axe", "level_req": 12, "stamina_cost": 65, # NEW GEAR
        "loot": [("mammoth_meat", 2, 0.4), ("crystal_salt", 2, 0.5), ("frozen_beans", 3, 0.6)],
        "messages": ["You braved the blizzard and found a massive, ancient beast.", "You chipped away rare, pure salt crystals from the ice.", "You harvested some hardy frozen beans that survived the cold."]
    },
    "volcano": { # NEW 4-STAR LOOT LOCATION
        "name": "Volcano Crater", "gear_req": "Heavy Duty Rifle", "level_req": 16, "stamina_cost": 80,
        "loot": [("volcanic_egg", 1, 0.3), ("red_peppers", 3, 0.6), ("nebula_spice", 1, 0.2)],
        "messages": ["The heat is almost unbearable, but you found a massive, steaming egg.", "You found a cluster of peppers that thrive in the heat."]
    },
    "sky_islands": { # NEW 5-STAR LOOT LOCATION
        "name": "Sky Islands", "gear_req": "Grappling Hook", "level_req": 20, "stamina_cost": 100, # NEW GEAR
        "loot": [("cloud_berries", 3, 0.5), ("sun_peaches", 2, 0.4), ("star_fruit", 1, 0.1)],
        "messages": ["You navigated the thin air and found floating islands of rare fruit.", "A quick grab before the cloud platform vanishes."]
    },
    "deep_sea": { # NEW 6-STAR LOOT LOCATION
        "name": "Deep Sea Trench", "gear_req": "Deep Sea Net", "level_req": 25, "stamina_cost": 120, # NEW GEAR
        "loot": [("abyssal_kelp", 3, 0.5), ("glacial_prawn", 1, 0.3), ("swamp_eel", 1, 0.5)],
        "messages": ["A flash of light revealed a massive prawn in the abyssal dark.", "You cast your net to pull up some strange kelp."]
    },
    "celestial_realm": { # NEW 7-STAR+ LOOT LOCATION
        "name": "Celestial Realm", "gear_req": "Exotic Net", "level_req": 30, "stamina_cost": 150,
        "loot": [("phoenix_ash", 1, 0.2), ("dragon_scale", 1, 0.1), ("crystal_salt", 3, 0.5)],
        "messages": ["You spotted an impossibly bright feather, leaving behind a pinch of ash.", "A shimmer in the air left a single, massive scale."]
    }
}

shop_items = {
    "flour": {"cost": 5}, "sugar": {"cost": 5}, "salt": {"cost": 3},
    "oil": {"cost": 8}, "potatoes": {"cost": 4},
    "coffee_beans": {"cost": 10}, "tea_leaves": {"cost": 7}
}

# --- HUNTING GEAR (EXPANDED) ---
shop_hunting_gear = {
    "basic_knife": {"name": "Basic Knife", "cost": 50, "level_req": 1},
    "sturdy_axe": {"name": "Sturdy Axe", "cost": 150, "level_req": 3},
    "hunting_rifle": {"name": "Hunting Rifle", "cost": 500, "level_req": 7},
    "ice_pick_axe": {"name": "Ice Pick Axe", "cost": 1200, "level_req": 12}, # NEW 4-STAR
    "heavy_duty_rifle": {"name": "Heavy Duty Rifle", "cost": 3000, "level_req": 16}, # NEW 5-STAR
    "grappling_hook": {"name": "Grappling Hook", "cost": 6000, "level_req": 20}, # NEW 6-STAR
    "deep_sea_net": {"name": "Deep Sea Net", "cost": 12000, "level_req": 25}, # NEW 7-STAR
    "exotic_net": {"name": "Exotic Net", "cost": 25000, "level_req": 30}, # NEW 8-STAR
    "legendary_bow": {"name": "Legendary Bow", "cost": 50000, "level_req": 40}, # NEW 9-STAR
    "master_trap": {"name": "Master Trap", "cost": 100000, "level_req": 50}, # NEW 10-STAR
}

# --- KITCHEN UPGRADES (EXPANDED) ---
shop_kitchen_upgrades = {
    # Cook Gear
    "iron_stove": {"name": "Iron Stove", "cost": 250, "level_req": 4, "star": 2},
    "chefs_oven": {"name": "Chef's Oven", "cost": 1000, "level_req": 8, "star": 3},
    "industrial_oven": {"name": "Industrial Oven", "cost": 2500, "level_req": 16, "star": 4}, # NEW 4-STAR
    "fusion_cooker": {"name": "Fusion Cooker", "cost": 5000, "level_req": 20, "star": 5}, # NEW 5-STAR
    "aether_oven": {"name": "Aether Oven", "cost": 15000, "level_req": 30, "star": 7}, # NEW 7-STAR
    "celestial_cooker": {"name": "Celestial Cooker", "cost": 50000, "level_req": 40, "star": 10}, # NEW 10-STAR

    # Drink Gear
    "kettle": {"name": "Kettle", "cost": 100, "level_req": 1, "star": 1, "type": "drink"},
    "industrial_brewer": {"name": "Industrial Brewer", "cost": 600, "level_req": 6, "star": 3, "type": "drink"}, # Made 3-star
    "advanced_brewer": {"name": "Advanced Brewer", "cost": 2000, "level_req": 14, "star": 5, "type": "drink"}, # NEW 5-STAR
    "master_brewer": {"name": "Master Brewer", "cost": 8000, "level_req": 22, "star": 8, "type": "drink"}, # NEW 8-STAR
    "divine_press": {"name": "Divine Press", "cost": 30000, "level_req": 35, "star": 10, "type": "drink"}, # NEW 10-STAR
}

# --- RECIPE BOOKS (EXPANDED) ---
shop_recipe_books = {
    "2_star_recipes": {"name": "2-Star Recipe Book", "cost": 200, "level_req": 4,
                       "unlocks": ["boar_roast", "truffle_pasta", "spicy_sausage"]},
    "1_star_drinks": {"name": "1-Star Drink Recipes", "cost": 50, "level_req": 1,
                      "unlocks": ["simple_coffee"]},
    "3_star_recipes_1": {"name": "3-Star Recipe Book (Vol 1)", "cost": 800, "level_req": 8,
                         "unlocks": ["venison_steak", "hearty_venison_chili", "energizing_latte"]}, # Added drink
    "3_star_recipes_2": {"name": "3-Star Recipe Book (Vol 2)", "cost": 2000, "level_req": 12,
                         "unlocks": ["eel_curry", "mammoth_tenderloin", "lunar_lime_pie", "elixir_of_life"]},
                         
    "4_star_recipes": {"name": "4-Star Recipe Book", "cost": 5000, "level_req": 16,
                       "unlocks": ["volcanic_stew", "cloudberry_tart", "seaweed_wrap", "nebula_tea"]}, # NEW
    "5_star_recipes": {"name": "5-Star Recipe Book", "cost": 10000, "level_req": 20,
                       "unlocks": ["prawn_cocktail", "sun_peach_sorbet", "phoenix_broth"]}, # NEW
    "6_star_recipes": {"name": "6-Star Recipe Book", "cost": 15000, "level_req": 25,
                       "unlocks": ["dragon_scale_soup", "star_fruit_jelly"]}, # NEW
    "7_star_recipes": {"name": "7-Star Recipe Book", "cost": 25000, "level_req": 30,
                       "unlocks": ["tier7_dish"]}, # NEW
    "8_star_recipes": {"name": "8-Star Recipe Book", "cost": 40000, "level_req": 35,
                       "unlocks": ["tier8_dish"]}, # NEW
    "9_star_recipes": {"name": "9-Star Recipe Book", "cost": 60000, "level_req": 40,
                       "unlocks": ["tier9_dish"]}, # NEW
    "10_star_recipes": {"name": "10-Star Recipe Book", "cost": 100000, "level_req": 50,
                       "unlocks": ["tier10_dish"]}, # NEW
}


# --- HELPER FUNCTIONS (UPDATED FOR NEW GEAR LOGIC) ---

def print_title(text):
    """Prints a formatted title."""
    print("\n" + "=" * (len(text) + 4))
    print(f"  {text}")
    print("=" * (len(text) + 4))

def clear_screen():
    """Simple way to clear the console for a cleaner look."""
    print("\n" * 50)

def check_level_up():
    """Checks if the player has enough XP to level up and handles it."""
    # Steeper XP requirement for the 10-star game
    xp_needed = player['level'] * 100
   
    if player['xp'] >= xp_needed:
        player['level'] += 1
        player['xp'] -= xp_needed
        player['max_stamina'] += 15
        player['stamina'] = player['max_stamina']
        print_title(f"*** LEVEL UP! You are now Level {player['level']}! ***")
        print(f"Your Max Stamina has increased to {player['max_stamina']}!")
        print("Your Stamina has been fully restored!")
        input("Press Enter to view your updated status...")
        print_status() # Automatically show status after level up
        return True
    return False

# FIX: Refactored to use the new separate gear keys
def get_kitchen_star_level():
    """Returns the star level (1-10) of the player's primary cooking gear."""
    gear_name = player["cooking_gear"]
    if gear_name == "Celestial Cooker": return 10
    if gear_name == "Aether Oven": return 7
    if gear_name == "Fusion Cooker": return 5
    if gear_name == "Industrial Oven": return 4
    if gear_name == "Chef's Oven": return 3
    if gear_name == "Iron Stove": return 2
    return 1 # Old Stove

# FIX: Refactored to use the new separate gear keys
def get_drink_star_level():
    """Returns the star level (0-10) of the player's drink-making gear."""
    gear_name = player["drink_gear"]
    if gear_name == "Divine Press": return 10
    if gear_name == "Master Brewer": return 8
    if gear_name == "Advanced Brewer": return 5
    if gear_name == "Industrial Brewer": return 3
    if gear_name == "Kettle": return 1
    return 0 # None

def spend_stamina(cost):
    """Checks and spends stamina. Returns True if successful."""
    if player['stamina'] < cost:
        print(f"You don't have enough stamina! (Need: {cost} STM, Have: {player['stamina']} STM)")
        print("You should 'sleep' to restore your stamina.")
        return False
    player['stamina'] -= cost
    return True

# --- CORE GAME FUNCTIONS ---

def do_hunt():
    """Handle the hunting sub-menu and action."""
    print_title("Go Hunting")
    print(f"Current Gear: {player['hunting_gear']} | Stamina: {player['stamina']}/{player['max_stamina']}")
    print("Where will you hunt?")

    location_options = []
    # Simplified check to see if the current gear is in the list of all gear equal or better than the requirement.
    gear_power = {v['name']: i for i, v in enumerate(shop_hunting_gear.values())}
    current_power = gear_power.get(player['hunting_gear'], 0)

    for i, (key, loc) in enumerate(hunt_locations.items(), 1):
        location_options.append(key)
       
        gear_req_power = gear_power.get(loc['gear_req'], 0)
        gear_req_met = current_power >= gear_req_power
       
        status = ""
        if player['level'] < loc['level_req']:
            status = f" (Requires Lvl {loc['level_req']}) ❌"
        elif not gear_req_met:
            status = f" (Requires {loc['gear_req']}) ❌"
        else:
            status = f" (Costs {loc['stamina_cost']} STM) ✅"
       
        print(f" [{i}] {loc['name']}{status}")
       
    print(" [0] Go Back")

    try:
        choice_str = input("> ")
        if choice_str == "0":
            return
           
        choice_index = int(choice_str) - 1
       
        if 0 <= choice_index < len(location_options):
            loc_key = location_options[choice_index]
            location = hunt_locations[loc_key]
           
            # --- Requirement Checks ---
            gear_req_power = gear_power.get(location['gear_req'], 0)
            gear_req_met = current_power >= gear_req_power
           
            if player['level'] < location['level_req']:
                print(f"You aren't high enough level for the {location['name']}.")
                return
            if not gear_req_met:
                print(f"You don't have the right gear! The {location['name']} requires a {location['gear_req']}.")
                return
            if not spend_stamina(location['stamina_cost']):
                return
               
            # --- Success: Go Hunting ---
            print(f"\nYou spend {location['stamina_cost']} stamina hunting in the {location['name']}...")
            time.sleep(1)
            print(random.choice(location['messages']))
            time.sleep(0.5)
           
            total_loot = []
            for (item, max_qty, chance) in location['loot']:
                if random.random() < chance:
                    amount = random.randint(1, max_qty) + 1
                    inventory[item] = inventory.get(item, 0) + amount
                    total_loot.append(f"{amount} {item.replace('_', ' ')}")
           
            if not total_loot:
                print("...but you came back empty-handed.")
            else:
                print(f"You found: {', '.join(total_loot)}!")
           
            player['xp'] += location['stamina_cost']
            check_level_up()
           
        else:
            print("That's not a valid location.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")

# FIX: do_cook now displays separated gear and checks against correct level.
def do_cook():
    """
    Handle the cooking sub-menu and mini-game, now also handling drinks.
    """
    print_title("Cook in Kitchen")
    # Display both gear types
    print(f"Current Cook Gear: {player['cooking_gear']} | Current Drink Gear: {player['drink_gear']}")
    print(f"Stamina: {player['stamina']}/{player['max_stamina']}")
   
    available_recipes = []
   
    meal_level = get_kitchen_star_level()
    drink_level = get_drink_star_level()
   
    # Filter known recipes based on available gear
    for key in known_recipes:
        recipe = recipes[key]
        recipe_type = recipe.get("type", "meal")
       
        # Check if the player has the right level gear for the recipe
        if recipe_type == "meal" and recipe['star'] <= meal_level:
            available_recipes.append(key)
        elif recipe_type == "drink" and recipe['star'] <= drink_level:
            available_recipes.append(key)
       
    if not available_recipes:
        print("You don't know any recipes you can cook with your current gear.")
        print("Buy a recipe book or upgrade your kitchen at the shop!")
        return

    print("What would you like to cook?")
    for i, key in enumerate(available_recipes, 1):
        recipe = recipes[key]
        recipe_type = recipe.get("type", "meal")
       
        # Print cooking location hint based on type
        location_hint = ""
        if recipe_type == "meal":
            if recipe['star'] == 1: location_hint = "(Old Stove)"
            elif recipe['star'] == 2: location_hint = "(Iron Stove)"
            elif recipe['star'] == 3: location_hint = "(Chef's Oven)"
            elif recipe['star'] == 4: location_hint = "(Industrial Oven)"
            elif recipe['star'] == 5 or recipe['star'] == 6: location_hint = "(Fusion Cooker)"
            elif recipe['star'] == 7 or recipe['star'] == 8 or recipe['star'] == 9: location_hint = "(Aether Oven)"
            elif recipe['star'] == 10: location_hint = "(Celestial Cooker)"
        else: # drink
            if recipe['star'] == 1: location_hint = "(Kettle)"
            elif recipe['star'] == 3: location_hint = "(Industrial Brewer)"
            elif recipe['star'] == 5: location_hint = "(Advanced Brewer)"
            elif recipe['star'] == 8: location_hint = "(Master Brewer)"
            elif recipe['star'] == 10: location_hint = "(Divine Press)"
       
        print(f" [{i}] {recipe['name']} ({recipe['star']}-Star {recipe_type.title()}) {location_hint} (Costs {recipe['stamina_cost']} STM/portion)")
       
        # Check if player has all required ingredients for ONE portion
        can_cook_one = True
        ingredient_str = []
        for item, amount_needed in recipe['ingredients'].items():
            amount_owned = inventory.get(item, 0)
            status = "✅"
            if amount_owned < amount_needed:
                can_cook_one = False
                status = "❌"
            ingredient_str.append(f"{item.replace('_', ' ')}: {amount_owned}/{amount_needed} {status}")
       
        print(f"     Ingredients: {', '.join(ingredient_str)}")
        if not can_cook_one:
            print("     (You don't have the ingredients for one portion!)")
   
    print(" [0] Go Back")
   
    # ... (Rest of do_cook remains the same, as it deals with input/output and inventory management) ...
    try:
        choice_str = input("> ")
        if choice_str == "0":
            return
           
        choice_index = int(choice_str) - 1
       
        if 0 <= choice_index < len(available_recipes):
            recipe_key = available_recipes[choice_index]
            recipe = recipes[recipe_key]
           
            # --- 1. Calculate Max Cookable Quantity (Batch Cooking) ---
            max_by_ingredients = sys.maxsize

            # Check ingredient limits for batch
            can_cook_any = True
            for item, amount_needed in recipe['ingredients'].items():
                amount_owned = inventory.get(item, 0)
                if amount_owned < amount_needed:
                    can_cook_any = False
                    break
               
                # Calculate how many portions this ingredient allows
                limit = amount_owned // amount_needed
                max_by_ingredients = min(max_by_ingredients, limit)

            if not can_cook_any:
                print("You don't have all the ingredients to cook even one portion.")
                return
           
            # Check stamina limit
            if recipe['stamina_cost'] > 0:
                max_by_stamina = player['stamina'] // recipe['stamina_cost']
            else:
                max_by_stamina = sys.maxsize

           
            max_cookable = min(max_by_ingredients, max_by_stamina)

            if max_cookable == 0:
                print(f"You don't have enough resources (ingredients or stamina) to cook even one portion.")
                return
           
            # --- 2. Ask for Quantity ---
            print(f"\nYou can cook up to {max_cookable} portions of {recipe['name']}.")
           
            try:
                amount_str = input(f"How many portions (1-{max_cookable}) do you want to cook? (Enter for Max) > ")
                if not amount_str:
                    amount = max_cookable
                else:
                    amount = int(amount_str)
            except ValueError:
                print("Invalid input. Please enter a whole number.")
                return

            if amount < 1 or amount > max_cookable:
                print(f"Invalid quantity. You must choose a number between 1 and {max_cookable}.")
                return
           
            # --- 3. Process Cooking ---

            total_stamina_cost = recipe['stamina_cost'] * amount
           
            if not spend_stamina(total_stamina_cost):
                return
           
            print(f"\nYou spend {total_stamina_cost} STM preparing {amount} portions of {recipe['name']}...")
           
            # Subtract ingredients (multiplied by amount)
            for item, amount_needed in recipe['ingredients'].items():
                inventory[item] -= amount_needed * amount
               
            # --- 4. The Single Mini-Game for all portions ---
            print("\n* FOCUS! Press Enter exactly when the 'GO!' appears. Your single reaction determines the quality of all portions. *")
           
            # Random wait time
            wait_time = random.uniform(1.5, 3.5)
            time.sleep(wait_time)
           
            # The prompt appears
            print("=" * 10)
            print("    !!! GO! !!!")
            print("=" * 10)
           
            start_time = time.time()
            input() # Wait for user to press Enter
            reaction_time = time.time() - start_time
           
            # Determine quality
            # Tighter window for Perfect: < 0.20s
            if reaction_time < 0.20:
                quality = "perfect"
                multiplier = 2.0
                print(f"\nINCREDIBLE! ({reaction_time:.3f}s) All {amount} portions are 'Perfect'!")
            elif reaction_time < 0.75:
                quality = "good"
                multiplier = 1.0
                print(f"\nNice! ({reaction_time:.3f}s) All {amount} portions are 'Good'.")
            else:
                quality = "poor"
                multiplier = 0.5
                print(f"\nFAILURE! ({reaction_time:.3f}s) All {amount} portions are 'Poor' quality.")
           
            # Add to cooked_meals inventory (multiplied by amount)
            if recipe_key not in cooked_meals:
                cooked_meals[recipe_key] = {"poor": 0, "good": 0, "perfect": 0}
            cooked_meals[recipe_key][quality] += amount
           
            # Grant XP (multiplied by amount)
            base_xp = recipe['xp'] * amount
            xp_gain = int(base_xp * multiplier)
            player['xp'] += xp_gain
            print(f"Gained {xp_gain} XP!")
            check_level_up()
           
        else:
            print("That's not a valid recipe number.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")


def do_sleep():
    """Restores stamina and advances to the next day."""
    print_title("End Day")
    print(f"You go to sleep for the night. (Day {player['day']})")
    time.sleep(1.5)
   
    # --- NEW ORDER SYSTEM: Fail/Clear Old Orders and Apply Penalties ---
    global active_orders
    if active_orders:
        print("\n--- Order Board Update ---")
        orders_to_clear = active_orders[:] # Copy the list to iterate
        active_orders = [] # Clear the board immediately
       
        for order in orders_to_clear:
            customer_key = order['customer_key']
            customer_name = customer_data.get(customer_key, {}).get("name", "Unknown Customer")
            penalty = customer_data.get(customer_key, {}).get("fail_penalty")
            recipe_name = recipes[order['recipe_key']]['name']
           
            print(f"❌ Failed to deliver {order['amount']}x {recipe_name} for customer **{customer_name}**.")
           
            # --- Apply Penalty Logic ---
            if penalty:
                penalty_type = penalty["type"]
                penalty_amount = penalty["amount"]
               
                if penalty_type == "money":
                    money_loss = int(player['money'] * penalty_amount)
                    player['money'] -= money_loss
                    print(f"    - Penalty: {customer_name} was furious! Lost **${money_loss}** ({int(penalty_amount * 100)}% of your money).")
                elif penalty_type == "money_fixed":
                    player['money'] -= penalty_amount
                    print(f"    - Penalty: {customer_name} charged a fee! Lost **${penalty_amount}**.")
                elif penalty_type == "xp":
                    player['xp'] -= penalty_amount
                    print(f"    - Penalty: {customer_name} spread a bad review! Lost **{penalty_amount} XP**.")
                    player['xp'] = max(0, player['xp']) # XP can't go below zero
                elif penalty_type == "max_stamina_temp":
                    # This is a 'temporary' penalty that will naturally reset by gaining max stamina back from level-ups.
                    # For simplicity here, we'll make it a permanent deduction unless the player levels up.
                    player['max_stamina'] = max(50, player['max_stamina'] - penalty_amount) # Cap at 50 to prevent soft-lock
                    player['stamina'] = min(player['stamina'], player['max_stamina'])
                    print(f"    - Penalty: {customer_name} caused intense stress! Max stamina reduced by **{penalty_amount}** to {player['max_stamina']}!")

        print("All outstanding orders have been cancelled.")
   
    # --- NEW ORDER SYSTEM: Check for new order with the Max 3 Order Limit ---
   
    # Determine the maximum number of allowed orders
    max_orders = 1 # Default max is 1, maintaining original game structure
    if player['max_stamina'] >= 225:
        max_orders = 3 # Increase max orders to 3 once stamina hits 225+
       
    # Check if a new order should be generated (50% chance, or guaranteed if board is empty and below max)
    if len(active_orders) < max_orders and (not active_orders or random.random() < 0.5):
        new_order = generate_customer_order()
        if new_order:
            active_orders.append(new_order)
            # Get the full customer name for the printout
            customer_name = customer_data.get(new_order['customer_key'], {}).get("name", "Unknown Customer")
            print(f"\n🔔 A new customer order has been posted: {new_order['amount']}x {recipes[new_order['recipe_key']]['name']} for **{customer_name}**!")
    else:
        # Inform the player if no new order came because of the limit
        if len(active_orders) >= max_orders:
            print(f"\nThe order board is full ({max_orders}/{max_orders}). No new orders posted.")

    player['day'] += 1
    player['stamina'] = player['max_stamina']
   
    print(f"It is now Day {player['day']}.")
    print(f"Your stamina has been fully restored to {player['stamina']}/{player['max_stamina']}.")
   

def go_shop():
    """Opens the shop menu."""
    print_title("WELCOME TO THE SHOP")
   
    while True:
        print(f"\nYour Money: ${player['money']} | Day: {player['day']}")
        print("[1] Buy Ingredients")
        print("[2] Sell Cooked Meals (Retail)")
        print("[3] View Order Board (Deliver Quests)") # Updated shop menu option
        print("--- UPGRADES ---")
        print("[4] Buy Hunting Gear")
        print("[5] Buy Cooking Gear (Stoves/Ovens)")
        print("[6] Buy Drink Gear (Kettles/Brewers)")
        print("[7] Buy Recipe Books")
        print("[0] Exit Shop")
       
        choice = input("> ")
       
        if choice == "1":
            buy_shop_items(shop_items, inventory, "Ingredients")
        elif choice == "2":
            sell_meals()
        elif choice == "3":
            handle_order_board() # New function
        elif choice == "4":
            # Pass hunting items and 'hunting_gear' key
            hunting_items = {k: v for k, v in shop_hunting_gear.items()}
            buy_shop_upgrades(hunting_items, "hunting_gear", "Hunting Gear")
        elif choice == "5":
            # Pass only the cooking items and 'cooking_gear' key
            cooking_items = {k: v for k, v in shop_kitchen_upgrades.items() if v.get('type') != 'drink'}
            buy_shop_upgrades(cooking_items, "cooking_gear", "Cooking Gear (Stoves/Ovens)")
        elif choice == "6":
            # Pass only the drink items and 'drink_gear' key
            drink_items = {k: v for k, v in shop_kitchen_upgrades.items() if v.get('type') == 'drink'}
            buy_shop_upgrades(drink_items, "drink_gear", "Drink Gear (Kettles/Brewers)")
        elif choice == "7":
            buy_recipe_books()
        elif choice == "0":
            print("Thanks for visiting the shop!")
            break
        else:
            print("Invalid choice. Please pick a number from the list.")

def buy_shop_items(item_list, target_inventory, title):
    """Generic function for buying stackable items."""
    print_title(f"Buy {title}")
   
    options = list(item_list.keys())
    for i, key in enumerate(options, 1):
        item = item_list[key]
        print(f" [{i}] {key.replace('_', ' ').title()} (${item['cost']} each)")
    print(" [0] Go Back")
       
    try:
        choice_str = input("What would you like to buy? > ")
        if choice_str == "0":
            return
           
        item_index = int(choice_str) - 1
       
        if 0 <= item_index < len(options):
            item_key = options[item_index]
            cost = item_list[item_key]['cost']
           
            max_buy = player['money'] // cost
            if max_buy == 0:
                print("You don't have enough money for even one of these.")
                return
               
            amount_str = input(f"How many {item_key.replace('_', ' ')} to buy? (Max: {max_buy}, Enter for Max) > ")
            if not amount_str:
                amount = max_buy
            else:
                amount = int(amount_str)
           
            if amount <= 0:
                print("Cancelling purchase.")
            elif amount > max_buy:
                print(f"You can only afford {max_buy}.")
            else:
                total_cost = cost * amount
                player['money'] -= total_cost
                target_inventory[item_key] = target_inventory.get(item_key, 0) + amount
                print(f"Bought {amount} {item_key.replace('_', ' ')} for ${total_cost}.")
        else:
            print("That's not a valid item number.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")

# FIX: Refactored logic to handle upgrades with separate keys
def buy_shop_upgrades(item_list, player_key, title):
    """Generic function for buying one-time upgrades."""
    print_title(f"Buy {title}")
   
    available_upgrades = []
    current_gear_name = player[player_key]
   
    # Logic for Hunting Gear (simple replacement)
    if player_key == "hunting_gear":
       
        # Get all gear names to determine current rank
        gear_rank_list = list(shop_hunting_gear.keys())
        current_rank = gear_rank_list.index(current_gear_name.lower().replace(' ', '_')) if current_gear_name.lower().replace(' ', '_') in gear_rank_list else -1

        for key, item in item_list.items():
            item_rank = gear_rank_list.index(key)
            if item_rank > current_rank:
                available_upgrades.append(item)
   
    # Logic for Cooking/Drink Gear (using star levels)
    elif player_key == "cooking_gear" or player_key == "drink_gear":
       
        # Determine the highest owned star level for the current category
        if player_key == "cooking_gear":
            current_star_level = get_kitchen_star_level()
            print(f"Your current Cook Gear: **{current_gear_name}** (Lvl {current_star_level})")
        else: # drink_gear
            current_star_level = get_drink_star_level()
            print(f"Your current Drink Gear: **{current_gear_name}** (Lvl {current_star_level})")

        # Filter items
        for item in item_list.values():
            if item['star'] > current_star_level:
                available_upgrades.append(item)
               
    else:
        print("Error: Unknown player_key for upgrade shop.")
        return

    # 2. Display and Handle Purchase
    if not available_upgrades:
        print("You already own the best available gear in this category!")
        return

    for i, item in enumerate(available_upgrades, 1):
        status = ""
        if player['level'] < item['level_req']:
            status = f" (Requires Lvl {item['level_req']}) ❌"
        elif player['money'] < item['cost']:
            status = f" (Can't afford) ❌"
        else:
            status = " (Available) ✅"
           
        print(f" [{i}] {item['name']} (${item['cost']}){status}")
    print(" [0] Go Back")
       
    try:
        choice_str = input("What would you like to buy? > ")
        if choice_str == "0":
            return
           
        item_index = int(choice_str) - 1
       
        if 0 <= item_index < len(available_upgrades):
            item_to_buy = available_upgrades[item_index]
           
            if player['level'] < item_to_buy['level_req']:
                print(f"You must be Level {item_to_buy['level_req']} to buy this.")
                return
            if player['money'] < item_to_buy['cost']:
                print("You don't have enough money for this.")
                return
               
            player['money'] -= item_to_buy['cost']
           
            # FIX: Simple replacement using the key
            player[player_key] = item_to_buy['name']
           
            print(f"\n*** Purchased the {item_to_buy['name']} for ${item_to_buy['cost']}! ***")
           
        else:
            print("That's not a valid item number.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")

def buy_recipe_books():
    """Specific function for buying recipe books."""
    print_title("Buy Recipe Books")
   
    available_books = []
    # Check if the first recipe in the book is known. If not, the book is available.
    for key, book in shop_recipe_books.items():
        # Check all recipes in the book; if ANY is unknown, the book is considered buyable
        is_unknown = False
        for recipe_key in book['unlocks']:
            if recipe_key not in known_recipes:
                is_unknown = True
                break
        if is_unknown:
            available_books.append(book)
           
    if not available_books:
        print("You already own all the recipe books!")
        return

    for i, book in enumerate(available_books, 1):
        status = ""
        if player['level'] < book['level_req']:
            status = f" (Requires Lvl {book['level_req']}) ❌"
        elif player['money'] < book['cost']:
            status = f" (Can't afford) ❌"
        else:
            status = " (Available) ✅"
           
        print(f" [{i}] {book['name']} (${book['cost']}){status}")
    print(" [0] Go Back")
       
    try:
        choice_str = input("What would you like to buy? > ")
        if choice_str == "0":
            return
           
        item_index = int(choice_str) - 1
       
        if 0 <= item_index < len(available_books):
            book_to_buy = available_books[item_index]
           
            if player['level'] < book_to_buy['level_req']:
                print(f"You must be Level {book_to_buy['level_req']} to buy this.")
                return
            if player['money'] < book_to_buy['cost']:
                print("You don't have enough money for this.")
                return
               
            player['money'] -= book_to_buy['cost']
           
            print(f"\n*** Purchased the {book_to_buy['name']} for ${book_to_buy['cost']}! ***")
            print("You learned new recipes:")
            for recipe_key in book_to_buy['unlocks']:
                if recipe_key not in known_recipes:
                    known_recipes.add(recipe_key)
                    print(f" - {recipes[recipe_key]['name']} ({recipes[recipe_key].get('type', 'meal').title()})")
           
        else:
            print("That's not a valid item number.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")


def sell_meals():
    """Sub-menu for selling cooked meals at retail (no quest/order)."""
    print_title("Sell Cooked Meals (Retail)")
   
    sellable_items = []
   
    for recipe_key, quality_dict in cooked_meals.items():
        for quality, count in quality_dict.items():
            if count > 0:
                base_val = recipes[recipe_key]['base_value']
               
                # Calculate value based on quality multiplier
                multiplier = 1.0
                if quality == "perfect": multiplier = 2.0
                elif quality == "poor": multiplier = 0.5
               
                value = int(base_val * multiplier)
                sellable_items.append((recipe_key, quality, count, value))
           
    if not sellable_items:
        print("You don't have any cooked meals to sell!")
        return
       
    for i, (r_key, qual, count, val) in enumerate(sellable_items, 1):
        name = recipes[r_key]['name']
        print(f" [{i}] {qual.title()} {name} (Have: {count}, Sell for: ${val} each)")
    print(" [0] Go Back")
       
    try:
        choice_str = input("What would you like to sell? > ")
        if choice_str == "0":
            return
           
        item_index = int(choice_str) - 1
       
        if 0 <= item_index < len(sellable_items):
            r_key, qual, max_sell, val = sellable_items[item_index]
            name = recipes[r_key]['name']
           
            amount_str = input(f"How many {qual} {name} to sell? (Max: {max_sell}, Enter for Max) > ")
            if not amount_str:
                amount = max_sell
            else:
                amount = int(amount_str)
           
            if amount <= 0:
                print("Cancelling sale.")
            elif amount > max_sell:
                print(f"You only have {max_sell} to sell.")
            else:
                total_sale = val * amount
                player['money'] += total_sale
                cooked_meals[r_key][qual] -= amount
                print(f"Sold {amount} {qual} {name} for ${total_sale}!")
                print(f"You now have ${player['money']}.")
        else:
            print("That's not a valid item number.")
           
    except ValueError:
        print("Invalid input. Please enter a number.")

# --- NEW ORDER SYSTEM: Functions (UPDATED LOGIC) ---

def generate_customer_order():
    """Generates a new order based on player level and known recipes."""
    # Only generate orders for recipes the player knows and can cook with current gear
    possible_recipes = []
   
    # NEW: Max star level scales with player level more gradually
    # Example: Lvl 1-4 -> 1-star, Lvl 5-9 -> 2-star, ..., Lvl 45-49 -> 10-star
    max_star_level = min(10, max(1, (player['level'] - 1) // 5 + 1))

    for key in known_recipes:
        recipe = recipes[key]
        if recipe['star'] <= max_star_level:
            possible_recipes.append(key)

    if not possible_recipes:
        return None
   
    # Select a recipe key
    recipe_key = random.choice(possible_recipes)
    recipe_star = recipes[recipe_key]['star']
   
    # Determine quantity (Higher level/star = bigger orders)
    base_qty = max(1, recipe_star // 2) # Base quantity is now based on half the star level (e.g., 3x for 6-star)
    amount = random.randint(base_qty, base_qty + 2)
   
    # Determine quality required (Higher star = higher chance of Perfect)
    # 1-star: < 10% perfect, 2-star: < 20% perfect, ..., 5-star: < 50% perfect
    if random.random() < (recipe_star / 10):
        quality_req = "perfect"
    elif random.random() < 0.85: # Increased chance for Good (85%)
        quality_req = "good"
    else:
        quality_req = "poor"
       
    # Calculate bonus reward (Higher bonus to incentivize orders over retail)
    retail_value = recipes[recipe_key]['base_value']
   
    # Calculate value based on quality multiplier for the base recipe
    multiplier = 1.0
    if quality_req == "perfect": multiplier = 2.0
    elif quality_req == "poor": multiplier = 0.5
   
    base_price = int(retail_value * multiplier)
    bonus_money = int(base_price * amount * 2.0) # **NEW: 100% bonus (2.0x multiplier)** on total sale
    bonus_xp = recipe_star * 30 * amount # Scaling XP reward, slightly higher
   
    # --- NEW: Use customer_data keys ---
    customer_key = random.choice(list(customer_data.keys()))
    customer_name = customer_data[customer_key]["name"]

    new_order = {
        "recipe_key": recipe_key,
        "amount": amount,
        "quality_req": quality_req,
        "money_reward": bonus_money,
        "xp_reward": bonus_xp,
        "customer_key": customer_key, # Store the key, not the name
        "customer_name": customer_name # Store the name for convenience
    }
   
    return new_order

# --- NEW: Dialogue function ---
def get_customer_dialogue(customer_key):
    """Returns a random dialogue line for the given customer key."""
    data = customer_data.get(customer_key)
    if data and data.get("dialogue"):
        return random.choice(data["dialogue"])
    return "A new order has arrived."
# --- END NEW: Dialogue function ---

def handle_order_board():
    """Displays active orders and allows the player to fulfill them."""
    print_title("CUSTOMER ORDER BOARD")
    global active_orders
   
    if not active_orders:
        print("The order board is empty. Try sleeping to see if a new order comes in!")
        return

    for i, order in enumerate(active_orders, 1):
        recipe = recipes[order['recipe_key']]
       
        # Check if player has the items needed to fulfill the order
        has_required = cooked_meals.get(order['recipe_key'], {}).get(order['quality_req'], 0)
        status = "✅" if has_required >= order['amount'] else "❌"
       
        # --- NEW: Print dialogue ---
        dialogue = get_customer_dialogue(order['customer_key'])
       
        print(f" [{i}] **Order from {order['customer_name']}** (STATUS: {status})")
        print(f"     *Customer says: \"{dialogue}\"*")
        print(f"     Requires: {order['amount']}x **{order['quality_req'].title()} {recipe['name']}**")
        print(f"     Reward: ${order['money_reward']} + {order['xp_reward']} XP")
        print(f"     (You have: {has_required} of required quality)")
       
    print(" [A] Attempt to fulfill an order (deliver)")
    print(" [0] Go Back")

    choice = input("> ").lower().strip()
   
    if choice == '0':
        return
    elif choice == 'a':
        try:
            order_choice_str = input("Enter the number of the order to fulfill > ")
            order_index = int(order_choice_str) - 1
           
            if 0 <= order_index < len(active_orders):
                order = active_orders[order_index]
                recipe_key = order['recipe_key']
                quality_req = order['quality_req']
                amount_req = order['amount']
               
                has_required = cooked_meals.get(recipe_key, {}).get(quality_req, 0)
               
                if has_required >= amount_req:
                    # Success! Fulfill the order
                   
                    # 1. Deduct items
                    cooked_meals[recipe_key][quality_req] -= amount_req
                   
                    # 2. Grant rewards
                    player['money'] += order['money_reward']
                    player['xp'] += order['xp_reward']
                   
                    # 3. Remove order
                    del active_orders[order_index]
                   
                    print_title("ORDER FULFILLED!")
                    # Use the stored customer name for the printout
                    print(f"Delivered {amount_req}x {quality_req.title()} {recipes[recipe_key]['name']} to {order['customer_name']}.")
                    print(f"Received **${order['money_reward']}** and **{order['xp_reward']} XP**.")
                    print(f"Money: ${player['money']} | XP: {player['xp']}")
                    check_level_up()
                   
                    if active_orders:
                        input("\nOrder board still has items. Press Enter to view...")
                        handle_order_board() # Recurse to show updated board
                   
                else:
                    print(f"You still need {amount_req - has_required} more {quality_req.title()} portions to complete this order.")
            else:
                print("Invalid order number.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Invalid choice.")


# --- END OF NEW ORDER SYSTEM FUNCTIONS ---


# FIX: print_status now shows separate kitchen gear.
def print_status():
    """Prints the player's current status and all inventories."""
    print_title(f"CHEF STATUS - DAY {player['day']} - Lvl {player['level']}")
    print(f"Money: ${player['money']} | Stamina: {player['stamina']}/{player['max_stamina']} STM")
   
    xp_needed = player['level'] * 100
   
    print(f"XP: {player['xp']}/{xp_needed} to Level {player['level'] + 1}")
    print(f"Gear: {player['hunting_gear']} (Hunting)")
    print(f"Gear: {player['cooking_gear']} (Cooking) / {player['drink_gear']} (Drink)")

    print("\n--- RAW INGREDIENTS ---")
    ingredient_list = []
    all_raw_items = {**inventory}

    for item, count in all_raw_items.items():
        if count > 0:
            ingredient_list.append(f"{item.replace('_', ' ').title()}: {count}")
   
    if not ingredient_list:
        print("Your pantry is empty.")
    else:
        print('\n'.join(ingredient_list))

    print("\n--- COOKED MEALS & DRINKS ---")
    meal_list = []
    for recipe_key, quality_dict in cooked_meals.items():
        for quality, count in quality_dict.items():
            if count > 0:
                name = recipes[recipe_key]['name']
                recipe_type = recipes[recipe_key].get('type', 'meal')
                meal_list.append(f"{quality.title()} {name} ({recipe_type.title()}): {count}")
    if not meal_list:
        print("You haven't cooked any meals or drinks.")
    else:
        print('\n'.join(meal_list))
       
    print("\n--- KNOWN RECIPES ---")
    kitchen_level = get_kitchen_star_level()
    drink_level = get_drink_star_level()
   
    for key in sorted(known_recipes, key=lambda r: recipes[r]['star']):
        recipe = recipes[key]
        recipe_type = recipe.get('type', 'meal')
       
        # Determine status based on type and level
        status = ""
        if recipe_type == 'meal':
            status_level = kitchen_level
            gear_name = 'Cook Gear'
        else: # drink
            status_level = drink_level
            gear_name = 'Drink Gear'
           
        status = "✅" if recipe['star'] <= status_level else f"❌ (Needs {recipe['star']}-Star {gear_name})"
       
        # Show ingredients for quick reference
        ingredients_short = ', '.join([f"{count} {item.replace('_', ' ')}" for item, count in recipe['ingredients'].items()])
        print(f" - {recipe['name']} ({recipe['star']}-Star {recipe_type.title()}) | Ingredients: {ingredients_short} {status}")

    # --- NEW ORDER SYSTEM: Status view ---
    print("\n--- ACTIVE ORDERS ---")
    if active_orders:
        for order in active_orders:
            print(f" - {order['amount']}x {order['quality_req'].title()} {recipes[order['recipe_key']]['name']} for {order['customer_name']} (Reward: ${order['money_reward']})")
    else:
        print("No active orders.")


# --- MAIN GAME LOOP ---
def main():
    """The main entry point for the game."""
    clear_screen()
    print_title("WELCOME TO THE CHEF SIM 2.0 (10-STAR EXPANSION)!")
    print("Goal: Reach Level 50 and get 225 stamina, do orders and make sure to read what type of food they want.") # Updated goal
    print("\nType 'help' for a list of commands.")
   
    while True:
        print("\n" + "-" * 40)
       
        order_status = f" | Orders: {len(active_orders)}" if active_orders else ""
        print(f"Day {player['day']} | STM: {player['stamina']}/{player['max_stamina']} | ${player['money']} | Lvl: {player['level']}{order_status}")
       
        # --- FIX: Added 'Orders' to the input prompt ---
        user_input = input("(Hunt, Cook, Shop, Orders, Sleep, Status, Help, Quit) > ").lower().strip()
       
        if user_input == "hunt" or user_input == "h":
            do_hunt()
       
        elif user_input == "cook" or user_input == "c":
            do_cook()
           
        elif user_input == "shop" or user_input == "s":
            go_shop()
           
        elif user_input == "orders" or user_input == "o": # New option for quick access
            handle_order_board()
               
        elif user_input == "sleep":
            do_sleep()
           
        elif user_input == "status" or user_input == "i":
            print_status()
           
        elif user_input == "help":
            print_title("COMMANDS")
            print(" - hunt (h): Go to one of five locations to find ingredients. (Costs STM)")
            print(" - cook (c): Prepare a meal or drink using the cooking mini-game. (Costs STM)")
            print(" - shop (s): Buy ingredients, gear, kitchen upgrades, or sell meals/access order board.")
            print(" - orders (o): View the active customer order board to deliver quests.")
            print(" - sleep: End the current day to restore all stamina and check for new orders.")
            print(" - status (i): Show your money, level, and all inventories.")
            print(" - help: Shows this list.")
            print(" - quit: Exit the game.")
           
           
        elif user_input == "quit":
            print("Thanks for playing, Chef!")
            break
           
        else:
            print("Unknown command. Type 'help' to see your options.")

# This makes the script runnable
if __name__ == "__main__":
    main()
