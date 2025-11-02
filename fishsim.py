import random
import time

# --- Game State Variables ---
game_state = {
    "location": "Pond",
    "money": 100,
    "xp": 0,
    "level": 1,
    "current_bait": "worm",
    "rod_name": "Basic Rod",
    "rod_power": 1.0,  # Must be a float for correct multiplication
    "time_of_day": "day",
    "unlocked_locations": {"Pond"},  # Tracks locations you've paid the one-time fee for
    "world": 1, # World 1 or 2
    # Store W1 rod to restore it when returning
    "w1_rod_power": 1.0,
    "w1_rod_name": "Basic Rod",
}

# Inventory stores individual fish objects
inventory = []

# --- World-Specific Inventories ---
special_items = {
    "world_2_key": 0
}
crafting_materials = {
    "wood_plank": 0,
    "iron_shard": 0,
    "beary_teddy": 0,
    "doggy": 0,
    "teddy": 0,
    "butterdoggy": 0,
    "mousey": 0,
    "melzie": 0,
    "whiteteddy": 0,
    "chicky": 0,
    "egg_chicky": 0,
    "little_teddy": 0,
    "burger": 0,
    "chips": 0,
    "nuggets": 0,
    "taco": 0,
    "burrito": 0,
    "toast": 0,
    "pizza": 0,
    "chicken": 0,
    "potatoes": 0,
    "orange": 0,
    "apple": 0,
    "guava": 0,
    "lime": 0,
    "avocado": 0,
    "blueberry": 0,
    "strawbery": 0,
    "melon": 0,
    "starfruit": 0,
    "pear": 0,
    "pomelo": 0,
    "banana": 0,
    "mango": 0,
    "lemon": 0,
    "cherry": 0,
    "grapes": 0,
    "pineapple": 0,
    "plum": 0,
    "apricot": 0,
    "peach": 0,
    "grapefruit": 0,
    "candy": 0,
    "lolly": 0,
    "lollipop": 0,
    "marshmallow": 0,
    "brownie": 0,
    "oreo": 0,
    "cake": 0,
    "donut": 0,
    "cupcake": 0,
    "cookie": 0,
    "gold": 0,
    "useless_thing":100000000000000
}

# --- World 1 Bait ---
bait_stock_w1 = {
    "worm": 10,
    "cricket": 0,
    "minnow": 0,
    "lure": 0,
    "glow_worm": 0,
    "deep_blob": 0,
    "tropical_bait": 0,
    "shrimp": 0
}
bait_data_w1 = {
    "worm": {"cost": 1, "catch_rate": 0.6, "night_bonus": 1.0},
    "cricket": {"cost": 3, "catch_rate": 0.75, "night_bonus": 1.0},
    "minnow": {"cost": 8, "catch_rate": 0.9, "night_bonus": 1.0},
    "lure": {"cost": 25, "catch_rate": 0.8, "night_bonus": 1.0},
    "glow_worm": {"cost": 10, "catch_rate": 0.7, "night_bonus": 1.5},
    "deep_blob": {"cost": 60, "catch_rate": 0.95, "night_bonus": 1.2},
    "tropical_bait": {"cost": 20, "catch_rate": 0.85, "night_bonus": 1.0},
    "shrimp": {"cost": 30, "catch_rate": 0.88, "night_bonus": 1.1},
}

# --- World 2 Bait ---
bait_stock_w2 = {
    "worm": 99999, # Infinite
    "power_bait": 0
}
bait_data_w2 = {
    # FIX APPLIED: Increased worm base catch rate to 0.5 for W2 playability.
    "worm": {"cost": 0, "catch_rate": 0.5, "night_bonus": 1.0, "notes": "Infinite supply in W2, now provides a decent base catch rate."},
    # FIX APPLIED: Massive boost to Power Bait catch rate to 0.95 for higher success chance.
    "power_bait": {"cost": 3, "catch_rate": 0.95, "night_bonus": 1.0, "notes": "Bought in packs. Helps reel in tough fish. (HUGE CATCH BOOST)"}
}
# --- Data Tables ---

locations = {
    # --- WORLD 1 ---
    "Pond": {
        "access_cost": 0, "level_req": 1, "difficulty": 1, "world": 1,
        "day_fish": ["minnows"]*5 + ["perch"]*3 + ["sunfish"]*2 + ["shiners", "catfish"],
        "night_fish": ["lanternfish"]*5 + ["eel"]*4 + ["catfish"],
    },
    "River": {
        "access_cost": 250, "level_req": 3, "difficulty": 3, "world": 1,
        "day_fish": ["perch"]*5 + ["sunfish"]*4 + ["shiners"]*4 + ["catfish", "trout", "salmon"],
        "night_fish": ["lanternfish"]*6 + ["eel"]*5 + ["catfish", "moonfish", "viperfish"],
    },
    "Lake": {
        "access_cost": 750, "level_req": 7, "difficulty": 5, "world": 1,
        "day_fish": ["catfish"]*6 + ["trout", "salmon", "bass"],
        "night_fish": ["eel"]*8 + ["bass", "moonfish", "stargazer"] + ["viperfish"]*2,
    },
    "Tropical Lagoon": {
        "access_cost": 2000, "level_req": 8, "difficulty": 7, "world": 1,
        "day_fish": ["parrotfish"]*7 + ["clown_snapper"]*2 + ["dolphin_fish", "dorado", "manta_ray"],
        "night_fish": ["parrotfish"]*5 + ["moonfish"]*3 + ["dorado", "reef_shark"],
    },
    "Ocean Coast": {
        "access_cost": 5000, "level_req": 12, "difficulty": 8, "world": 1,
        "day_fish": ["mackerel"]*7 + ["bluefish", "snapper", "dolphin_fish", "dorado", "tuna"],
        "night_fish": ["eel"]*7 + ["moonfish", "viperfish", "shark", "swordfish"],
    },
    "Deep Sea Trench": {
        "access_cost": 15000, "level_req": 20, "difficulty": 12, "world": 1,
        "day_fish": ["anglerfish"]*7 + ["oarfish"]*2 + ["giant_grouper", "colossal_squid"],
        "night_fish": ["anglerfish", "viperfish", "giant_grouper", "colossal_squid"] + ["vampire_squid"]*5,
    },
    "Arctic Ice Shelf": {
        "access_cost": 35000, "level_req": 25, "difficulty": 15, "world": 1,
        "day_fish": ["polar_cod"]*4 + ["ice_cod", "arctic_chub"],
        "night_fish": ["arctic_char"]*5 + ["seal", "penguin", "ice_shrimp", "killer_whale"],
    },
    "Volcanic Hotspot": {
        "access_cost": 80000, "level_req": 35, "difficulty": 18, "world": 1,
        "day_fish": ["thermal_trout"]*5 + ["lava_eel"]*2 + ["fire_bass"]*2 + ["magma_shark"],
        "night_fish": ["lava_eel"]*5 + ["pyro_snapper"]*5 + ["magma_shark", "obsidian_fish"],
    },
    "Subterranean Cave": {
        "access_cost": 250000, "level_req": 50, "difficulty": 25, "world": 1,
        "day_fish": ["tetra"]*9 + ["tiger_shark", "goliath_grouper", "abyssal_eel"],
        "night_fish": ["isopod"]*6 + ["tetra", "black_bream", "goliath_grouper"],
    },
    "Emoji Island": {
        "access_cost": 1000000, "level_req": 60, "difficulty": 30, "world": 1,
        "day_fish": ["happy_fish"]*40 + ["sad_fish"]*30 + ["angry_fish"]*29 + ["golden_emoji"],
        "night_fish": ["laughing_fish"]*40 + ["crying_fish"]*30 + ["devil_fish"]*29 + ["golden_emoji"],
    },
    "World 2 Portal": {
        "access_cost": 0, "level_req": 1, "difficulty": 0, "world": 1,
        "is_portal": True, "target_world": 2, "target_loc": "Wood Wood",
        "day_fish": [], "night_fish": [],
    },

    # --- WORLD 2 ---
    "Wood Wood": {
        "access_cost": 0, "level_req": 1, "difficulty": 8, "world": 2,
        # Wood Plank drop fish now set to a 10/100 weight each (7.0% chance per cast).
        "is_shop": True,
        "day_fish": ["Random log"]*76 + ["Tree"]*10 + ["Laughing tree"]*8 + ["Dead tree"]*4 + ["Tree already caught"]*2,
        "night_fish": ["Random log"]*76 + ["Underground Tree"]*10 + ["Flying sleeping tree"]*8 + ["Dead tree"]*4 + ["Tree already caught"]*2,
    },
       "Iron Iron": {
        "access_cost": 150, "level_req": 1, "difficulty": 8, "world": 2,
        # Iron in your hand is 17/100 weight (11.9% catch chance).
        "day_fish": ["Fighting Iron"]*59 + ["Flying Iron"]*20 + ["Running Iron"]*15 + ["Iron"]*4 + ["Iron in your hand"]*2,
        "night_fish": ["Fighting Iron"]*59 + ["Iron already ate"]*20 + ["Hiding Iron"]*15 + ["Iron"]*4 + ["Iron in your hand"]*2,
    },
    "Beary Beary": {
       "access_cost": 150, "level_req": 1, "difficulty": 12, "world": 2,
        # TOTAL WEIGHT NOW 14. Air fish are now 86 (46+40).
        "day_fish": ["Air"]*54 + ["Breathed in air"]*40 + ["Beary eating you"]*2 + ["Beary"]*2 + ["Lotsa beary skin"]*2,
        "night_fish": ["Air"]*54 + ["Breathed in air"]*40 + ["Beary eating you"]*2 + ["Beary"]*2 + ["Lotsa beary skin"]*2,
    },
    "The Workshop": {
        "access_cost": 0, "level_req": 1, "difficulty": 0, "world": 2, "is_crafting_area": True,
        "day_fish": [], "night_fish": [],
    },
    "Teddy Wild": {
        "access_cost": 10, "level_req": 10, "difficulty": 20, "world": 2,
        "day_fish": ["Teddy"]*10 + ["Doggy"]*10 + ["Butterdoggy"]*10 + ["Beary"]*10 + ["Mousey"]*10 + ["Melzie"]*10 +["Whiteteddy"]*10 + ["Chicky"]*10 + ["Egg chicky"]*10 + ["Little teddy"]*10,
        "night_fish": ["Teddy"]*10 + ["Doggy"]*10 + ["Butterdoggy"]*10 + ["Beary"]*10 + ["Mousey"]*10 + ["Melzie"]*10 +["Whiteteddy"]*10 + ["Chicky"]*10 + ["Egg chicky"]*10 + ["Little teddy"]*10,
    },
    "Food": {
        "access_cost": 10, "level_req": 15, "difficulty": 20, "world": 2,
        "day_fish": ["Hamburger"]*10 + ["Chips"]*10 + ["Nuggets"]*10 + ["Taco"]*10 + ["Burrito"]*10 + ["Toast"]*10 + ["Pizza"]*10 + ["Chicken"]*10 + ["Potatoes"]*10 + ["Orange"]*10,
        "night_fish": ["Hamburger"]*10 + ["Chips"]*10 + ["Nuggets"]*10 + ["Taco"]*10 + ["Burrito"]*10 + ["Toast"]*10 + ["Pizza"]*10 + ["Chicken"]*10 + ["Potatoes"]*10 + ["Orange"]*10,
    },    
    "Fruit": {
    "access_cost": 10, "level_req": 15, "difficulty": 20, "world": 2,
    "day_fish": ["Apple"]*10 + ["Guava"]*10 + ["Lime"]*10 + ["Avocado"]*10 + ["Blueberries"]*10 + ["Strawberry"]*10 + ["Watermelon"]*10 + ["Starfruit"]*10 + ["Pear"]*10 + ["Pomelo"],
    "night_fish": ["Banana"]*10 + ["Mango"]*10 + ["Lemon"]*10 + ["Cherries"]*10 + ["Grapes"]*10 + ["Pineapple"]*10 + ["Plum"]*10 + ["Apricot"]*10 + ["Peach"]*10 + ["Grapefruit"]
    },
    "Sweet Food": {
    "access_cost": 100, "level_req": 15, "difficulty": 20, "world": 2,
    "day_fish": ["Candy"]*10 + ["Lolly"]*10 + ["Lollipop"]*10 + ["Marshmallow"]*10 + ["Brownie"]*10 + ["Oreo"]*10 + ["Cake"]*10 + ["Donut"]*10 + ["Cupcake"]*10 + ["Cookie"],
    "night_fish": ["Candy"]*10 + ["Lolly"]*10 + ["Lollipop"]*10 + ["Marshmallow"]*10 + ["Brownie"]*10 + ["Oreo"]*10 + ["Cake"]*10 + ["Donut"]*10 + ["Cupcake"]*10 + ["Cookie"],
    },
    "Lotsa Money Grind": {
    "access_cost": 100, "level_req": 15, "difficulty": 20, "world": 2,
    "day_fish": ["There_is_one_legendary_0.01percent"]*999 + ["LEGENDARY TEDDY!!!!"]*1,
    "night_fish": ["There_is_one_legendary_0.01percent"]*9999 + ["LEGENDARY TEDDY!!!!"]*1,
    },

    "World 1 Portal": {
        "access_cost": 0, "level_req": 1, "difficulty": 0, "world": 2,
        "is_portal": True, "target_world": 1, "target_loc": "Pond",
        "day_fish": [], "night_fish": [],
    },
}

fish_data = {
    # FIX: Added rarity to high-tier W1 fish for more engaging feedback.
    # Pond/River/Lake Species
    "minnows": {"base_value": 3, "min_weight": 0.1, "max_weight": 0.5, "xp_per_lb": 1, "rarity": "common"},
    "perch": {"base_value": 5, "min_weight": 0.2, "max_weight": 0.8, "xp_per_lb": 3, "rarity": "common"},
    "shiners": {"base_value": 7, "min_weight": 0.3, "max_weight": 1.0, "xp_per_lb": 8, "rarity": "common"},
    "lanternfish": {"base_value": 8, "min_weight": 0.4, "max_weight": 1.5, "xp_per_lb": 9, "rarity": "common"},
    "eel": {"base_value": 10, "min_weight": 0.5, "max_weight": 3.0, "xp_per_lb": 10, "rarity": "common"},
    "sunfish": {"base_value": 12, "min_weight": 0.5, "max_weight": 2.0, "xp_per_lb": 10, "rarity": "common"},
    "catfish": {"base_value": 15, "min_weight": 1.0, "max_weight": 5.0, "xp_per_lb": 12, "rarity": "rare"},
    "trout": {"base_value": 25, "min_weight": 2.0, "max_weight": 8.0, "xp_per_lb": 18, "rarity": "rare"},
    "viperfish": {"base_value": 30, "min_weight": 3.0, "max_weight": 9.0, "xp_per_lb": 20, "rarity": "rare"},
    "moonfish": {"base_value": 35, "min_weight": 4.0, "max_weight": 12.0, "xp_per_lb": 22, "rarity": "rare"},
    "bass": {"base_value": 40, "min_weight": 3.0, "max_weight": 10.0, "xp_per_lb": 25, "rarity": "rare"},
    "salmon": {"base_value": 50, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 27, "rarity": "rare"},
    "stargazer": {"base_value": 60, "min_weight": 6.0, "max_weight": 18.0, "xp_per_lb": 29, "rarity": "epic"},
    # Ocean Coast Species
    "mackerel": {"base_value": 18, "min_weight": 1.5, "max_weight": 6.0, "xp_per_lb": 15, "rarity": "common"},
    "bluefish": {"base_value": 38, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 25, "rarity": "uncommon"},
    "snapper": {"base_value": 45, "min_weight": 7.0, "max_weight": 20.0, "xp_per_lb": 30, "rarity": "uncommon"},
    "dolphin_fish": {"base_value": 55, "min_weight": 10.0, "max_weight": 30.0, "xp_per_lb": 15, "rarity": "rare"},
    "dorado": {"base_value": 65, "min_weight": 12.0, "max_weight": 40.0, "xp_per_lb": 32, "rarity": "rare"},
    "tuna": {"base_value": 80, "min_weight": 20.0, "max_weight": 50.0, "xp_per_lb": 34, "rarity": "rare"},
    "shark": {"base_value": 75, "min_weight": 30.0, "max_weight": 60.0, "xp_per_lb": 36, "rarity": "rare"},
    "swordfish": {"base_value": 100, "min_weight": 50.0, "max_weight": 80.0, "xp_per_lb": 37, "rarity": "epic"},
    # Deep Sea Trench Species
    "anglerfish": {"base_value": 150, "min_weight": 100.0, "max_weight": 150.0, "xp_per_lb": 32, "rarity": "rare"},
    "oarfish": {"base_value": 120, "min_weight": 80.0, "max_weight": 200.0, "xp_per_lb": 44, "rarity": "epic"},
    "giant_grouper": {"base_value": 200, "min_weight": 150.0, "max_weight": 300.0, "xp_per_lb": 0.2, "rarity": "epic"},
    "colossal_squid": {"base_value": 180, "min_weight": 200.0, "max_weight": 400.0, "xp_per_lb": 0.3, "rarity": "epic"},
    "vampire_squid": {"base_value": 50, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 2, "rarity": "rare"},
    # Tropical Lagoon
    "parrotfish": {"base_value": 28, "min_weight": 4.0, "max_weight": 12.0, "xp_per_lb": 22, "rarity": "uncommon"},
    "clown_snapper": {"base_value": 40, "min_weight": 6.0, "max_weight": 25.0, "xp_per_lb": 30, "rarity": "uncommon"},
    "manta_ray": {"base_value": 220, "min_weight": 60.0, "max_weight": 180.0, "xp_per_lb": 32, "rarity": "epic"},
    "reef_shark": {"base_value": 90, "min_weight": 25.0, "max_weight": 80.0, "xp_per_lb": 35, "rarity": "rare"},
    # Arctic Ice Shelf
    "polar_cod": {"base_value": 22, "min_weight": 2.0, "max_weight": 203.0, "xp_per_lb": 9, "rarity": "common"},
    "ice_cod": {"base_value": 35, "min_weight": 5.0, "max_weight": 603.0, "xp_per_lb": 12, "rarity": "uncommon"},
    "arctic_chub": {"base_value": 45, "min_weight": 50.0, "max_weight": 700.0, "xp_per_lb": 0.1, "rarity": "rare"},
    "arctic_char": {"base_value": 65, "min_weight": 10.0, "max_weight": 50.0, "xp_per_lb": 9, "rarity": "uncommon"},
    "seal": {"base_value": 150, "min_weight": 200.0, "max_weight": 500.0, "xp_per_lb": 4, "rarity": "rare"},
    "penguin": {"base_value": 80, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 4, "rarity": "rare"},
    "killer_whale": {"base_value": 500, "min_weight": 500.0, "max_weight": 1000.0, "xp_per_lb": 0.1, "rarity": "epic"},
    # Volcanic Hotspot Species
    "thermal_trout": {"base_value": 70, "min_weight": 5.0, "max_weight": 25.0, "xp_per_lb": 4, "rarity": "uncommon"},
    "lava_eel": {"base_value": 110, "min_weight": 15.0, "max_weight": 50.0, "xp_per_lb": 12, "rarity": "rare"},
    "fire_bass": {"base_value": 140, "min_weight": 20.0, "max_weight": 60.0, "xp_per_lb": 1, "rarity": "rare"},
    "magma_shark": {"base_value": 250, "min_weight": 100.0, "max_weight": 350.0, "xp_per_lb": 0.05, "rarity": "epic"},
    "pyro_snapper": {"base_value": 170, "min_weight": 25.0, "max_weight": 80.0, "xp_per_lb": 1, "rarity": "rare"},
    "obsidian_fish": {"base_value": 400, "min_weight": 400.0, "max_weight": 700.0, "xp_per_lb": 0.02, "rarity": "epic"},
    # Subterranean Cave Species
    "tetra": {"base_value": 90, "min_weight": 1.0, "max_weight": 5.0, "xp_per_lb": 2, "rarity": "common"},
    "tiger_shark": {"base_value": 350, "min_weight": 300.0, "max_weight": 800.0, "xp_per_lb": 0.05, "rarity": "epic"},
    "goliath_grouper": {"base_value": 550, "min_weight": 600.0, "max_weight": 1200.0, "xp_per_lb": 0.05, "rarity": "epic"},
    "abyssal_eel": {"base_value": 800, "min_weight": 1000.0, "max_weight": 2000.0, "xp_per_lb": 0.01, "rarity": "epic"},
    "isopod": {"base_value": 100, "min_weight": 0.5, "max_weight": 2.0, "xp_per_lb": 2, "rarity": "common"},
    "black_bream": {"base_value": 150, "min_weight": 100.0, "max_weight": 150.0, "xp_per_lb": 0.5, "rarity": "rare"},
    # Emoji Island
    "happy_fish": {"base_value": 100, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 20, "rarity": "common"},
    "sad_fish": {"base_value": 120, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 22, "rarity": "common"},
    "angry_fish": {"base_value": 150, "min_weight": 7.0, "max_weight": 15.0, "xp_per_lb": 25, "rarity": "common"},
    "laughing_fish": {"base_value": 110, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 20, "rarity": "common"},
    "crying_fish": {"base_value": 130, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 22, "rarity": "common"},
    "devil_fish": {"base_value": 160, "min_weight": 7.0, "max_weight": 15.0, "xp_per_lb": 25, "rarity": "common"},
    "golden_emoji": {"base_value": 10000, "min_weight": 750, "max_weight": 800, "xp_per_lb": 100, "rarity": "legendary", "special_drop": "world_2_key"},
# --- World 2 Fish (The ONLY keys for W2 fish in fish_data) ---
# Each of these funny names represents a tier of fish stats/drops.

    "Random log": {"base_value": 5, "min_weight": 1.0, "max_weight": 5.0, "xp_per_lb": 2, "rarity": "common"},
    "Tree": {
    "base_value": 5, "min_weight": 2.0, "max_weight": 10.0, "xp_per_lb": 3, "rarity": "common",
    "drop": "wood_plank", "drop_chance": 0.15
    },
    "Fighting Iron": {
    "base_value": 10, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 5, "rarity": "uncommon",
    "drop": "iron_shard", "drop_chance": 0.05
    },
    "Beary eating you": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0, "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "beary_teddy", "drop_chance": 0.20
    },
    "Teddy": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "teddy", "drop_chance": 0.15
    },
    "Doggy": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "doggy", "drop_chance": 0.15  
    },
    "Beary": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "beary_teddy", "drop_chance": 0.15  
    },
    "Butterdoggy": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "butterdoggy", "drop_chance": 0.15  
    },
    "Mousey": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "mousey", "drop_chance": 0.15  
    },
    "Melzie": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "melzie", "drop_chance": 0.15  
    },
    "Whiteteddy": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "whiteteddy", "drop_chance": 0.15  
    },
    "Chicky": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "chicky", "drop_chance": 0.15  
    },
    "Egg chicky": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "egg_chicky", "drop_chance": 0.15  
    },
    "Little teddy": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "very_rare",
    "drop": "little_teddy", "drop_chance": 0.15  
    },
    "Hamburger": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "burger", "drop_chance": 0.10
    },
    "Chips": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "chips", "drop_chance": 0.10
    },
    "Nuggets": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "nuggets", "drop_chance": 0.10
    },
    "Taco": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "taco", "drop_chance": 0.10
    },
    "Burrito": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "burrito", "drop_chance": 0.10
    },
    "Toast": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "toast", "drop_chance": 0.10
    },
    "Pizza": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "pizza", "drop_chance": 0.10
    },
    "Chicken": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "chicken", "drop_chance": 0.10
    },
    "Potatoes": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "potatoes", "drop_chance": 0.10
    },
    "Orange": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "orange", "drop_chance": 0.10
    },
    "Apple": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 70.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "apple", "drop_chance": 0.10
    },
    "Guava": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "guava", "drop_chance": 0.10
    },
    "Lime": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "lime", "drop_chance": 0.10
    },
    "Avocado": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "avocado", "drop_chance": 0.10
    },
    "Blueberries": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "blueberry", "drop_chance": 0.10
    },
    "Strawberry": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "strawberry", "drop_chance": 0.10
    },
    "Watermelon": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "melon", "drop_chance": 0.10
    },
    "Starfruit": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "starfruit", "drop_chance": 0.10
    },
    "Pear": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "pear", "drop_chance": 0.10
    },
    "Pomelo": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "pomelo", "drop_chance": 0.10
    },
    "Banana": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "banana", "drop_chance": 0.10
    },
    "Mango": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "mango", "drop_chance": 0.10
    },
    "Lemon": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "lemon", "drop_chance": 0.10
    },
    "Cherries": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "cherry", "drop_chance": 0.10
    },
    "grapes": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "grapes", "drop_chance": 0.10
    },
    "Pineapple": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "pineapple", "drop_chance": 0.10
    },
    "Plum": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "plum", "drop_chance": 0.10
    },
    "Apricot": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "apricot", "drop_chance": 0.10
    },
    "Peach": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "peach", "drop_chance": 0.10
    },
    "Grapefruit": {
    "base_value": 50, "min_weight": 20.0, "max_weight": 50.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "grapefruit", "drop_chance": 0.10
    },
    "Candy": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "candy", "drop_chance": 0.15
    },
    "Lolly": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "lolly", "drop_chance": 0.15
    },
    "Lollipop": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "lollipop", "drop_chance": 0.15
    },
    "Marshmallow": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "marshmallow", "drop_chance": 0.15
    },
    "Brownie": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "brownie", "drop_chance": 0.15
    },
    "Oreo": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "oreo", "drop_chance": 0.15
    },
    "Cake": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "cake", "drop_chance": 0.15
    },
    "Donut": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "donut", "drop_chance": 0.15
    },
    "Cupcake": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "cupcake", "drop_chance": 0.15
    },
    "Cookie": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "cookie", "drop_chance": 0.15
    },
    "There_is_one_legendary_0.01percent": {
    "base_value": 75, "min_weight": 100.0, "max_weight": 150.0,  "xp_per_lb": 1, "rarity": "common",
    "drop": "useless_thing", "drop_chance": 100
    },
    "LEGENDARY TEDDY!!!!": {
    "base_value": 75, "min_weight": 20.0, "max_weight": 75.0,  "xp_per_lb": 5000, "rarity": "legendary",
    "drop": "gold", "drop_chance": 100
    },

}

# --- World 2 Fish Mapping ---
# This dictionary links all the specific funny names from location lists
# to the ONE funny name that holds the actual stats in fish_data.
w2_fish_map = {
    # All logs map to the stats of "Random log" or "Tree" (wood plank drop)
    "Dead tree": "Random log",
    "Underground Tree": "Random log",
    "Laughing tree": "Tree",
    "Flying sleeping tree": "Tree",
    "Tree already caught": "Tree",
   
    # All Iron fish map to the stats of "Fighting Iron" (iron shard drop)
    "Flying Iron": "Fighting Iron",
    "Hiding Iron": "Fighting Iron",
    "Running Iron": "Fighting Iron",
    "Iron": "Fighting Iron",
    "Iron already ate": "Fighting Iron",
    "Iron in your hand": "Fighting Iron",

    # All Beary fish map to the stats of "Beary eating you" (beary teddy drop)
    # FIX APPLIED: Mapped all Beary fish to the correct stats key
    "Air": "Random log", # 'Air' and 'Breathed in air' are low-tier fish
    "Breathed in air": "Random log",
    "Beary eating you": "Beary eating you", # Maps to itself
    "Beary": "Beary eating you",            
    "Lotsa beary skin": "Beary eating you", # Maps to Beary eating you

    "Teddy": "Teddy",
    "Doggy": "Doggy",
    "Butterdoggy": "Butterdoggy",
    "Mousey": "Mousey",
    "Melzie": "Melzie",
    "Whiteteddy": "Whiteteddy",
    "Chicky": "Chicky",
    "Egg chicky": "Egg chicky",
    "Little teddy": "Little teddy",
}

def get_fish_stats(fish_name):
    """Retrieves the stats for a given fish name."""
   
    # World 2 Logic: Check the map first for funny names
    if game_state["world"] == 2 and fish_name in w2_fish_map:
        # If it's a funny name in the map (e.g., 'Laughing tree'), use the real data key ('Tree').
        real_fish_name = w2_fish_map[fish_name]
        return fish_data.get(real_fish_name)
   
    # World 1 Logic & World 2 Fallback: Check the fish_data directly
    # This handles all World 1 fish (like 'Perch') AND the W2 fish names that are direct keys in fish_data (like 'Random log').
    return fish_data.get(fish_name)

# NOTE: The rest of the functions like calculate_catch() will follow this function.



# --- WORLD 1 RODS ---
rod_upgrades_w1 = {
    2: {"name": "Fiberglass Rod", "cost": 150, "rod_power": 1.5, "level_req": 2, "world": 1},
    3: {"name": "Graphite Rod", "cost": 400, "rod_power": 2.0, "level_req": 5, "world": 1},
    4: {"name": "Titanium Rod", "cost": 1500, "rod_power": 3.0, "level_req": 9, "world": 1},
    5: {"name": "Carbon Fiber Rod", "cost": 4500, "rod_power": 4.0, "level_req": 14, "world": 1},
    6: {"name": "Electric Reel", "cost": 12000, "rod_power": 5.0, "level_req": 18, "world": 1},
    7: {"name": "Hydro-Drive Reel", "cost": 40000, "rod_power": 6.5, "level_req": 22, "world": 1},
    8: {"name": "Quantum Reel", "cost": 120000, "rod_power": 7.5, "level_req": 30, "world": 1},
    9: {"name": "Lightning Rod", "cost": 500000, "rod_power": 8.0, "level_req": 50, "world": 1},
    10: {"name": "Zapper Rod", "cost": 750000, "rod_power": 9.0, "level_req": 75, "world": 1},
    11: {"name": "Jotham's Rod", "cost": 1500000, "rod_power": 10.0, "level_req": 125, "world": 1},
    12: {"name": "Jerome's Rod", "cost": 2500000, "rod_power": 15.0, "level_req": 150, "world": 1},
    13: {"name": "Jairus's Reel", "cost": 7500000, "rod_power": 16.0, "level_req": 175, "world": 1},
    15: {"name": "Jairus's Proper Reel", "cost": 25000000, "rod_power": 20.0, "level_req": 200, "world": 1},
    16: {"name": "Smiley Rod", "cost": 3000000, "rod_power": 25.0, "level_req": 70, "world": 1},
    17: {"name": "Angry Rod", "cost": 9000000, "rod_power": 30.0, "level_req": 80, "world": 1},
}

# --- WORLD 2 RODS (CRAFTABLE) ---
rod_upgrades_w2 = {
    1: {"name": "Broken Rod", "rod_power": 0.5, "level_req": 1, "world": 2, "craftable": False},
   
    2:{"name": "Normal Rod", "cost": 500, "rod_power": 7.5, "level_req": 1, "world": 2, "craftable": False},

    3: {"name": "Useless Rod", "rod_power": 0.51, "level_req": 1, "world": 2, "craftable": True,
    "recipe": {"useless_thing": 100000000000000}},
    4: {"name": "Beary Rod", "rod_power": 10.0, "level_req": 1, "world": 2, "craftable": True,
        "recipe": {"wood_plank": 5, "iron_shard": 3, "beary_teddy": 1}},
    5: {"name": "Little Teddy Rod", "rod_power": 15.0, "level_req": 5, "world": 2, "craftable": True,
        "recipe": {"wood_plank": 5, "iron_shard": 1, "little_teddy": 5}},
    6: {"name": "Teddy Rod", "rod_power": 20.0, "level_req": 10, "world": 2, "craftable": True,
        "recipe": {"chicky": 5, "butterdoggy": 5, "teddy": 5, "doggy": 5}},
    7: {"name": "Cold Rod", "rod_power": 25.0, "level_req": 15, "world": 2, "craftable": True,
        "recipe": {"whiteteddy": 10, "mousey": 5, "melzie": 5, "egg_chicky": 1}},
    8: {"name": "Food Rod", "rod_power": 30.0, "level_req": 25, "world": 2, "craftable": True,
        "recipe": {"potatoes": 15, "burrito": 5, "taco": 5, "burger": 5, "chips": 5}},
    9: {"name": "Fruit Rod", "rod_power": 35.0, "level_req": 30, "world": 2, "craftable": True,
     "recipe": {"apple": 15, "lemon": 10, "melon": 10, "plum": 5, "pear": 5}},
    10: {"name": "Candy Rod", "rod_power": 40.0, "level_req": 45, "world": 2, "craftable": True,
     "recipe": {"cookie": 50}},
    11: {"name": "Grind Rod", "rod_power": 500.0, "level_req": 45, "world": 2, "craftable": True,
     "recipe": {"gold": 1}},
   
   
}


# --- Core Mechanics ---
# --- ADMIN COMMAND ---
def admin_get_rod(rod_name_key):
    """Grants a specific rod and its required crafting materials."""
    global game_state, crafting_materials

    # Standardize rod name for dictionary lookup
    rod_name_formatted = rod_name_key.replace('_', ' ').title()
   
    rod_data = None
    for tier, data in rod_upgrades_w2.items():
        if data["name"] == rod_name_formatted:
            rod_data = data
            break

    if not rod_data:
        print(f"Admin Error: Rod '{rod_name_formatted}' not found in W2 upgrades.")
        return

    # 1. Grant the materials for the rod (if it has a recipe)
    if rod_data.get("craftable", False) and "recipe" in rod_data:
        print(f"Granting materials for {rod_data['name']}...")
        for item, amount in rod_data["recipe"].items():
            crafting_materials[item] = max(crafting_materials.get(item, 0), amount)
            print(f" - Granted {amount} of {item.replace('_', ' ')}")

    # 2. Grant the rod itself (updates current rod only if better)
    if rod_data["rod_power"] > game_state["rod_power"]:
        game_state["rod_power"] = rod_data["rod_power"]
        game_state["rod_name"] = rod_data["name"]
        print(f"\n*** CHEAT: Equipped {game_state['rod_name']}! (Power: {game_state['rod_power']}) ***")
    else:
        print(f"\nCHEAT: {rod_data['name']} is weaker or equal to your current rod ({game_state['rod_name']}). Materials granted.")


def admin_skip_w2():
    # ... (Keep existing admin_skip_w2 function as is)
    pass
def get_current_bait_stock():
    return bait_stock_w1 if game_state["world"] == 1 else bait_stock_w2

def get_current_bait_data():
    return bait_data_w1 if game_state["world"] == 1 else bait_data_w2

def get_current_rod_upgrades():
    return rod_upgrades_w1 if game_state["world"] == 1 else rod_upgrades_w2

def toggle_time_of_day():
    if game_state["time_of_day"] == "day":
        game_state["time_of_day"] = "night"
        print("\n*** The sun sets, and it is now NIGHT. Time for the nocturnal fish! ***")
    else:
        game_state["time_of_day"] = "day"
        print("\n*** The sun rises, and it is now DAY. ***")

def check_level_up():
    while game_state["xp"] >= game_state["level"] * 50:
        game_state["xp"] -= game_state["level"] * 50
        game_state["level"] += 1
        print(f"\n*** LEVEL UP! You are now Level {game_state['level']}! ***")
        print("Your reeling skill has improved — fish struggle less against you!")

def calculate_catch():
    current_location_data = locations[game_state["location"]]
   
    if game_state["time_of_day"] == "day":
        possible_fish = current_location_data["day_fish"]
    else:
        possible_fish = current_location_data["night_fish"]

    if not possible_fish:
        print("There are no fish here at this time.")
        return None

    # --- FIX APPLIED HERE: Fixed Catch Chance ---
    # The chance of success (not seaweed) is fixed at 70% (1.0 - 0.3)
    catch_chance = 0.7
    # The previous complex calculation has been removed to enforce the 30% seaweed rule.
    # Note: This is a major simplification. Bait and level no longer affect the chance
    # of getting a bite, but bait is still consumed (unless W2 worm).
    # ---------------------------------------------

    if random.random() > catch_chance:
        print("...nothing but seaweed. The fish aren't biting.")
        return None

    fish_name = random.choice(possible_fish)
    data = get_fish_stats(fish_name)
   
    # Add a check for valid fish data
    if data is None or not isinstance(data, dict):
        # Fallback stats to prevent crash if fish data is bad
        print(f"Error: Could not retrieve valid fish data for {fish_name}. Using fallback stats.")
        # Create a default dictionary to avoid a crash
        data = {"max_weight": 1.0, "min_weight": 0.1, "base_value": 1, "xp_per_lb": 1}

    # The Rod Power is still used to increase the size/value of the fish
    max_w = data["max_weight"] * game_state["rod_power"]
    min_w = data["min_weight"]
    if min_w > max_w:
        min_w = max_w / 2

    weight = round(random.uniform(min_w, max_w), 2)

    base_value = data["base_value"]
    selling_value = int(base_value * weight * random.uniform(0.9, 1.1))

    return {"type": fish_name, "weight": weight, "value": selling_value}
def go_shop():
    if game_state["world"] == 2 and not locations[game_state["location"]].get("is_shop", False):
        print("The only shop in this world is at 'Wood Wood'.")
        return
       
    if game_state["world"] == 1:
        print("\n--- TACKLE SHOP (WORLD 1) ---")
        shop_loop_w1()
    elif game_state["world"] == 2:
        print("\n--- TRADING POST (WORLD 2) ---")
        shop_loop_w2()

def start_fishing():
    current_bait_stock = get_current_bait_stock()
   
    if current_bait_stock[game_state["current_bait"]] <= 0:
        print(f"You are out of {game_state['current_bait']}! Change bait or buy more.")
        return
       
    if not locations[game_state["location"]]["day_fish"] and not locations[game_state["location"]]["night_fish"]:
        print("You can't fish here.")
        return

    if not (game_state["world"] == 2 and game_state["current_bait"] == "worm"):
        current_bait_stock[game_state["current_bait"]] -= 1

    print(f"Casting line with {game_state['current_bait']} at the {game_state['location']} during {game_state['time_of_day']}...")
    time.sleep(1)

    bite_time = random.randint(3, 8) / max(1, game_state["level"])
    print(f"Waiting for a bite... (Est. {round(bite_time, 1)}s)")
    time.sleep(bite_time)

    catch_result = calculate_catch()

    if catch_result is None:
        print("The fish got away.")
        toggle_time_of_day()
        return

    fish_name = catch_result["type"]
    weight = catch_result["weight"]
    selling_value = catch_result["value"]
    # REPLACE WITH THIS ROBUST BLOCK:
    fish_info = get_fish_stats(fish_name)
   
    # Check if the returned data is a dictionary. If not, use a fallback.
    if fish_info and isinstance(fish_info, dict):
        fish_rarity = fish_info.get("rarity", "common")
        xp_gained = int(weight * fish_info.get("xp_per_lb", 0))
    else:
        # Fallback in case of bad or missing data
        print(f"Warning: Could not get valid data for {fish_name}. Using default values.")
        fish_rarity = "common"
        xp_gained = 0
       
    print(f"\n!!! FISH ON! It feels like a {fish_name.upper()} of {weight} lbs! Estimated value: ${selling_value}! !!!")
    print(f"(Rarity: {fish_rarity.title()})")

    base_reeling_difficulty = weight * locations[game_state["location"]]["difficulty"] / max(0.0001, game_state["rod_power"])
    level_effect = 1.0 + (game_state["level"] - 1) * 0.05
    level_effect = min(level_effect, 25.0)
    reeling_difficulty = base_reeling_difficulty / level_effect

    bait_bonus_msg = ""
    if game_state["world"] == 2 and fish_rarity == "very_rare":
        if game_state["current_bait"] == "worm":
            reeling_difficulty *= 25
            bait_bonus_msg = " (Buy power bait and equip power bait, right now you are on HARD mode because you don't have power bait or equipped it.)"
        elif game_state["current_bait"] == "power_bait":
            reeling_difficulty /= 5
            bait_bonus_msg = " (Power Bait is helping!)"

    success_bar = 0
    max_bar = 100

    input("Press ENTER to start reeling!")
    start_time = time.time()

    while success_bar < max_bar and time.time() - start_time < 10:
        player_reels = random.randint(10, 20) * game_state["rod_power"]
        success_bar += player_reels

        low_bound = max(1, int(reeling_difficulty / 2))
        high_bound = max(low_bound, int(reeling_difficulty))
        fish_struggle = random.randint(low_bound, high_bound)

        rod_effect = 1.0 + (game_state["rod_power"] - 1.0) * 0.1
        fish_struggle = int(fish_struggle / rod_effect)
        fish_struggle = max(1, fish_struggle)

        success_bar -= fish_struggle
        success_bar = max(0, min(max_bar, success_bar))

        bar_width = 20
        filled = int(success_bar * bar_width / max_bar)
        bar = '█' * filled + '░' * (bar_width - filled)

        print(f"  > Reeling... [{bar}] {int(success_bar)}/{max_bar} | Struggle: -{fish_struggle}{bait_bonus_msg}")
        time.sleep(0.5)

    if success_bar >= max_bar:
        # FIX: NOW CALLS THE NEW FUNCTION
        xp_gained = int(weight * get_fish_stats(fish_name)["xp_per_lb"])
        inventory.append(catch_result)
        game_state["xp"] += xp_gained
        print(f"\nSuccess! You landed a {weight} lb {fish_name.title().replace('_', ' ')}!")
        print(f"Gained {xp_gained} XP!")
       
        # FIX: NOW CALLS THE NEW FUNCTION
        fish_info = get_fish_stats(fish_name)
       
        if "special_drop" in fish_info and fish_info["special_drop"] == "world_2_key":
            if special_items["world_2_key"] == 0:
                special_items["world_2_key"] = 1
                print("\n*** You find a strange glowing key ***")
                print("A new location has appeared on your map: 'World 2 Portal'")
               
        if "drop" in fish_info and random.random() < fish_info.get("drop_chance", 0):
            item_dropped = fish_info["drop"]
            crafting_materials[item_dropped] += 1
            print(f"The {fish_name.title().replace('_', ' ')} dropped 1 {item_dropped.replace('_', ' ')}!")

        check_level_up()
    else:
        print("\nOh no! The line snapped and the fish got away.")

    toggle_time_of_day()
# --- Shop and Inventory ---

def shop_loop_w1():
    global game_state
    current_bait_data = get_current_bait_data()
    current_bait_stock = get_current_bait_stock()
   
    while True:
        print(f"\nMoney: ${game_state['money']} | Level: {game_state['level']} | Rod: {game_state['rod_name']} ({game_state['rod_power']})")
        print("[1] Buy Bait (World 1)")
        print("[2] Sell Catch")
        print("[3] Buy Rod Upgrades (World 1)")
        print("[0] Exit Shop")
        choice = input("> ")

        if choice == "1":
            print("\n--- Buy Bait (World 1) ---")
            bait_list = list(current_bait_data.keys())
            for i, bait_name in enumerate(bait_list, 1):
                data = current_bait_data[bait_name]
                notes = data.get("notes", "")
                if "night_bonus" in data and data["night_bonus"] > 1.0:
                    notes = (notes + " (Night catch bonus!)").strip()
                print(f" [{i}] {bait_name.title().replace('_', ' ')} (Cost: ${data['cost']}) Stock: {current_bait_stock[bait_name]} {notes}")

            try:
                bait_choice_str = input(f"Select bait (1-{len(bait_list)}, 0 to cancel): ")
                if bait_choice_str == "0": continue
                bait_choice = int(bait_choice_str)
                bait_name = bait_list[bait_choice - 1]
                cost = current_bait_data[bait_name]["cost"]
                if cost == 0:
                    print("You can't buy this item.")
                    continue

                max_buy = game_state['money'] // cost
                if max_buy == 0:
                    print("You don't have enough money for one.")
                    continue
                   
                amount_str = input(f"How many {bait_name} to buy? (Max: {max_buy}, 0 to cancel): ")
                if amount_str == "0": continue
                amount = int(amount_str)
                total_cost = amount * cost

                if total_cost > game_state["money"]:
                    print("You don't have enough money!")
                elif amount > 0:
                    game_state["money"] -= total_cost
                    current_bait_stock[bait_name] += amount
                    print(f"Bought {amount} {bait_name} for ${total_cost}. Stock: {current_bait_stock[bait_name]}")
                else:
                    print("Invalid amount.")
            except (ValueError, IndexError):
                print("Invalid input.")

        elif choice == "2":
            sell_fish()

        elif choice == "3":
            print("\n--- Buy Rod Upgrades (World 1) ---")
            current_rods = get_current_rod_upgrades()
            upgrade_options = []
            for tier, data in current_rods.items():
                # Show only W1 rods that are better than the player's current W1 rod
                if data["rod_power"] > game_state["w1_rod_power"]:
                    upgrade_options.append(data)
           
            upgrade_options.sort(key=lambda x: x['rod_power'])

            if not upgrade_options:
                print("You already own the highest available rod in this world.")
                continue

            for i, data in enumerate(upgrade_options, 1):
                print(f" [{i}] {data['name']} (Power: {data['rod_power']} | Cost: ${data['cost']} | Level Req: {data['level_req']})")
            try:
                upgrade_choice = input(f"Enter the number of the upgrade to buy (1-{len(upgrade_options)}, 0 to cancel): ")
                if upgrade_choice == "0":
                    continue

                selected_upgrade = upgrade_options[int(upgrade_choice) - 1]

                # Check all conditions before purchase
                if game_state["level"] < selected_upgrade["level_req"]:
                    print(f"You need to be Level {selected_upgrade['level_req']} to buy this rod.")
                elif game_state["money"] < selected_upgrade["cost"]:
                    print(f"You need ${selected_upgrade['cost']} to buy the {selected_upgrade['name']}.")
                else:
                    # All checks passed, process the purchase
                    game_state["money"] -= selected_upgrade["cost"]
                    game_state["rod_power"] = selected_upgrade["rod_power"]
                    game_state["rod_name"] = selected_upgrade["name"]
                   
                    # Also update the stored W1 rod to remember the upgrade
                    game_state["w1_rod_power"] = selected_upgrade["rod_power"]
                    game_state["w1_rod_name"] = selected_upgrade["name"]
                   
                    print(f"\n*** Purchased {selected_upgrade['name']}! Your rod power is now {game_state['rod_power']}. ***")

            except (ValueError, IndexError):
                print("Invalid input.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def shop_loop_w2():
    global game_state
    current_bait_stock = get_current_bait_stock()
   
    while True:
        print(f"\nMoney: ${game_state['money']} | Level: {game_state['level']} | Rod: {game_state['rod_name']} ({game_state['rod_power']})")
        print("[1] Buy Bait Packs (World 2)")
        print("[2] Sell Catch")
        print("[3] Buy Rod Upgrades (World 2)")
        print("[0] Exit Shop")
        choice = input("> ")

        if choice == "1":
            print("\n--- Buy Bait Packs (World 2) ---")
            print(f"Money: ${game_state['money']}")
            print(f"[1] 50 Power Bait Pack (Cost: $150)")
            print("[0] Back")
           
            pack_choice = input("> ")
            if pack_choice == "1":
                cost = 150
                amount = 50
                if game_state["money"] < cost:
                    print("Not enough money for a pack.")
                else:
                    game_state["money"] -= cost
                    current_bait_stock["power_bait"] += amount
                    print(f"Bought {amount} Power Bait for ${cost}. Stock: {current_bait_stock['power_bait']}")
            elif pack_choice == "0":
                continue
            else:
                print("Invalid choice.")

        elif choice == "2":
            sell_fish()
           
        elif choice == "3": # Logic for buying W2 rods
            print("\n--- Buy Rod Upgrades (World 2) ---")
            current_rods = get_current_rod_upgrades()
            upgrade_options = []
           
            # Filter for W2 rods that are NOT craftable and are better than current rod
            for tier, data in current_rods.items():
                if data["world"] == 2 and not data.get("craftable", True) and data["rod_power"] > game_state["rod_power"]:
                    upgrade_options.append(data)
           
            upgrade_options.sort(key=lambda x: x['rod_power'])

            if not upgrade_options:
                print("No buyable rod upgrades available that are better than your current rod.")
                continue

            for i, data in enumerate(upgrade_options, 1):
                print(f" [{i}] {data['name']} (Power: {data['rod_power']} | Cost: ${data['cost']} | Level Req: {data['level_req']})")
           
            try:
                upgrade_choice = input(f"Enter the number of the upgrade to buy (1-{len(upgrade_options)}, 0 to cancel): ")
                if upgrade_choice == "0":
                    continue

                selected_upgrade = upgrade_options[int(upgrade_choice) - 1]

                # Check all conditions before purchase
                if game_state["level"] < selected_upgrade["level_req"]:
                    print(f"You need to be Level {selected_upgrade['level_req']} to buy this rod.")
                elif game_state["money"] < selected_upgrade["cost"]:
                    print(f"You need ${selected_upgrade['cost']} to buy the {selected_upgrade['name']}.")
                else:
                    # All checks passed, process the purchase
                    game_state["money"] -= selected_upgrade["cost"]
                    game_state["rod_power"] = selected_upgrade["rod_power"]
                    game_state["rod_name"] = selected_upgrade["name"]
                   
                    print(f"\n*** Purchased {selected_upgrade['name']}! Your rod power is now {game_state['rod_power']}. ***")

            except (ValueError, IndexError, KeyError):
                print("Invalid input.")
       
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def sell_fish():
    global game_state
    if not inventory:
        print("Your cooler is empty. No fish to sell.")
        return

    total_sale = 0
    print("\n--- Selling Inventory ---")

    fish_summary = {}
    for fish in inventory:
        fish_summary.setdefault(fish['type'], []).append(fish)
        total_sale += fish['value']

    for fish_type, fish_list in fish_summary.items():
        count = len(fish_list)
        total_value = sum(f['value'] for f in fish_list)
        print(f" - Sold {count} {fish_type.title().replace('_', ' ')}(s) for ${total_value}")

    game_state["money"] += total_sale
    inventory.clear()
    print(f"\nTotal sale: ${total_sale}. Current Money: ${game_state['money']}")

def change_location(new_location_args):

   
    new_location_key = " ".join(new_location_args).title()
   

    if new_location_key not in locations:
        print(f"Unknown location. Use the 'locations' command to see available spots.")
        return

    data = locations[new_location_key]

    if new_location_key == game_state["location"]:
        print(f"You are already at the {new_location_key}.")
        return
       
    if new_location_key == "World 2 Portal" and special_items["world_2_key"] == 0:
        print("You haven't found the key to unlock this portal.")
        return
       
    if data["world"] != game_state["world"]:
        print(f"You can't travel to '{new_location_key}' from this world.")
        print("Use a Portal to change worlds.")
        return

    if game_state["level"] < data["level_req"]:
        print(f"You must be Level {data['level_req']} to travel to the {new_location_key}.")
        return

    if data.get("is_portal", False):
        print(f"Activating portal to World {data['target_world']}...")
        time.sleep(1)
       
        if data["target_world"] == 2:
            print("The world shifts around you... Your old gear feels useless here!")
            # Store W1 rod (already updated by shop)
            # Set W2 default rod
            game_state["rod_power"] = rod_upgrades_w2[1]["rod_power"]
            game_state["rod_name"] = rod_upgrades_w2[1]["name"]
            game_state["current_bait"] = "worm"
            print(f"You arrive with a {game_state['rod_name']} (Power: {game_state['rod_power']}).")
            print("You'll need to craft new rods to progress.")

        elif data["target_world"] == 1:
            print("You return to the familiar world...")
            # Restore W1 rod
            game_state["rod_power"] = game_state.get("w1_rod_power", 1.0)
            game_state["rod_name"] = game_state.get("w1_rod_name", "Basic Rod")
            game_state["current_bait"] = "worm"
            print(f"You equip your {game_state['rod_name']} (Power: {game_state['rod_power']}).")
       
        game_state["world"] = data["target_world"]
        game_state["location"] = data["target_loc"]
        print(f"Traveled to {game_state['location']} in World {game_state['world']}.")
        return

    if new_location_key in game_state["unlocked_locations"]:
        game_state["location"] = new_location_key
        print(f"Traveled to the {new_location_key}.")
    else:
        if game_state["money"] < data["access_cost"]:
            print(f"You need ${data['access_cost']} to unlock the {new_location_key}.")
            return

        game_state["money"] -= data["access_cost"]
        game_state["location"] = new_location_key
        game_state["unlocked_locations"].add(new_location_key)
        print(f"Purchased access to the {new_location_key} for ${data['access_cost']}!")

    print(f"You are now at the {game_state['location']}.")

def change_bait(new_bait_args):
    new_bait_key = "_".join(new_bait_args)
   
    current_bait_data = get_current_bait_data()
    current_bait_stock = get_current_bait_stock()

    if new_bait_key not in current_bait_data:
        print(f"Unknown bait for this World. Available: {', '.join(b.replace('_', ' ') for b in current_bait_data.keys())}")
        return

    if current_bait_stock[new_bait_key] <= 0:
        print(f"You are out of {new_bait_key.title().replace('_', ' ')}. Visit the shop to buy more.")
        return

    game_state["current_bait"] = new_bait_key
    print(f"Switched bait to {new_bait_key.title().replace('_', ' ')}.")

def craft_rod(rod_key_args):
    if game_state["world"] != 2:
        print("You can only craft in World 2.")
        return
       
    if not locations[game_state["location"]].get("is_crafting_area", False):
        print("You must be at 'The Workshop' to craft.")
        return
       
    rod_to_craft = None
    rod_name_formatted = " ".join(rod_key_args).title()
   
    for tier, data in rod_upgrades_w2.items():
        if data["name"] == rod_name_formatted:
            rod_to_craft = data
            break
           
    if not rod_to_craft:
        print(f"Unknown craftable rod: {rod_name_formatted}")
        return
       
    if not rod_to_craft.get("craftable", False):
        print(f"You cannot craft the {rod_name_formatted}.")
        return
       
    recipe = rod_to_craft["recipe"]
    can_craft = True
    print(f"\n--- Crafting: {rod_to_craft['name']} ---")
    print(f"Requires:")
    for item, amount in recipe.items():
        has_amount = crafting_materials.get(item, 0)
        req_met_str = "✅" if has_amount >= amount else "❌"
        print(f" - {item.replace('_', ' ')}: {has_amount} / {amount} {req_met_str}")
        if has_amount < amount:
            can_craft = False
           
    if game_state["level"] < rod_to_craft["level_req"]:
        print(f"Level Requirement: {game_state['level']} / {rod_to_craft['level_req']} ❌")
        can_craft = False
    else:
        print(f"Level Requirement: {game_state['level']} / {rod_to_craft['level_req']} ✅")
       
    if rod_to_craft["rod_power"] <= game_state["rod_power"]:
        print("You already have a rod that is this good or better. ❌")
        can_craft = False
       
    if not can_craft:
        print("\nCannot craft item. Missing requirements.")
        return
       
    print("\nCrafting...")
    for item, amount in recipe.items():
        crafting_materials[item] -= amount
       
    game_state["rod_power"] = rod_to_craft["rod_power"]
    game_state["rod_name"] = rod_to_craft["name"]
    print(f"*** Success! Crafted {game_state['rod_name']}! (Power: {game_state['rod_power']}) ***")

# --- ADMIN COMMAND ---

def admin_skip_w2():
    """Sets the game state as if the player just entered World 2 via the portal."""
    global game_state, special_items
   
    # 1. Simulate finding the key
    special_items["world_2_key"] = 1
   
    # 2. Simulate entering the portal (using the same logic as change_location)
    game_state["world"] = 2
    game_state["location"] = "Wood Wood"
   
    # 3. Simulate World 2 Rod setup
    w2_default_rod = rod_upgrades_w2[1]
    game_state["rod_power"] = w2_default_rod["rod_power"]
    game_state["rod_name"] = w2_default_rod["name"]
    game_state["current_bait"] = "worm"
   
    # 4. Optional: Give some cash and bait for a quick start
    game_state["money"] += 500
    bait_stock_w2["power_bait"] += 100
   
    print("~" * 60)
    print("--- ADMIN SKIP: WELCOME TO WORLD 2 ---")
    print("World 2 Key acquired. W1 Rod stored. Starting location set.")
    print(f"You have been granted ${500} and 100 Power Bait.")
    print(f"Current Rod: {game_state['rod_name']} (Power: {game_state['rod_power']})")
    print("~" * 60)

# --- UI and Helper Functions ---

def print_status():
    print("\n--- ANGLER STATUS ---")
    print(f"Time of Day: {game_state['time_of_day'].upper()}")
    print(f"WORLD: {game_state['world']}")
    print(f"Location: {game_state['location']} (Difficulty {locations[game_state['location']]['difficulty']})")
    print(f"Money: ${game_state['money']}")
    print(f"Level: {game_state['level']} (XP: {game_state['xp']}/{game_state['level'] * 50})")
    print(f"Rod: {game_state['rod_name']} (Power: {game_state['rod_power']})")
    print(f"Current Bait: {game_state['current_bait'].title().replace('_', ' ')}")

    print("\n--- INVENTORY (Cooler) ---")
    fish_summary = {}
    for fish in inventory:
        fish_summary.setdefault(fish['type'], []).append(fish)

    if not fish_summary:
        print("Cooler is empty.")
    else:
        for fish_type, fish_list in fish_summary.items():
            count = len(fish_list)
            total_weight = sum(f['weight'] for f in fish_list)
            total_value = sum(f['value'] for f in fish_list)
            print(f" - {fish_type.title().replace('_', ' ')} ({count}): {round(total_weight, 2)} lbs total (Est. ${total_value})")

    print("\n--- BAIT BOX ---")
    current_bait_stock = get_current_bait_stock()
    has_bait = False
    for bait, qty in current_bait_stock.items():
        if qty > 0:
            qty_str = "Infinite" if bait == "worm" and game_state["world"] == 2 else qty
            print(f" - {bait.title().replace('_', ' ')}: {qty_str}")
            has_bait = True
    if not has_bait:
        print("Bait box is empty.")
       
    if game_state["world"] == 2:
        print("\n--- CRAFTING MATERIALS ---")
        has_mats = False
        for item, qty in crafting_materials.items():
            if qty > 0:
                print(f" - {item.replace('_', ' ')}: {qty}")
                has_mats = True
        if not has_mats:
            print("No materials.")
           
        print("\n--- CRAFTABLE RODS (at 'The Workshop') ---")
        for tier, data in rod_upgrades_w2.items():
            if data.get("craftable", False) and data["rod_power"] > game_state["rod_power"]:
                print(f" - {data['name']} (Power: {data['rod_power']}, Lvl: {data['level_req']})")
                recipe_str = ", ".join([f"{v} {k.replace('_', ' ')}" for k, v in data["recipe"].items()])
                print(f"   Recipe: {recipe_str}")
               
    print("\n--- SPECIAL ITEMS ---")
    has_special = False
    if special_items["world_2_key"] > 0:
        print(" - World 2 Key (Portal is active!)")
        has_special = True
    if not has_special:
        print("No special items.")


def print_help():
    print("\n--- Commands ---")
    print(" **fish / f** : Cast your line. **Toggles Day/Night.**")
    print(" **shop / s** : Go to the shop (Shop location varies by world).")
    print(" **go <location>** : Travel to a new fishing spot (e.g., go ocean coast).")
    print(" **bait <type>** : Change your current bait (e.g., bait minnow).")
    print(" **status / i** : Show your money, level, inventory, and bait stock.")
    print(" **locations** : View fishing spots in your *current world*.")
    print(" **help** : Show this list of commands.")
    if game_state["world"] == 2:
        print(" **craft <rod name>** : Craft a new rod at 'The Workshop' (e.g., craft beary rod).")
    print(" **quit** : Exit the game.")

def print_locations():
    print(f"\n--- Fishing Locations (WORLD {game_state['world']}) ---")
    for name, data in locations.items():
        if data["world"] != game_state['world']:
            continue
           
        if name == "World 2 Portal" and special_items["world_2_key"] == 0:
            continue
           
        is_unlocked = "✅ UNLOCKED" if name in game_state["unlocked_locations"] or data["access_cost"] == 0 else f"❌ LOCKED (Fee: ${data['access_cost']})"
       
        notes = ""
        if data.get("is_portal", False):
            notes = f" (Portal to World {data['target_world']})"
        elif data.get("is_shop", False):
            notes = " (W2 Shop Location)"
        elif data.get("is_crafting_area", False):
            notes = " (W2 Crafting Location)"

        print(f"\n - {name}{notes}")
        print(f"   {is_unlocked} | Level Req: {data['level_req']} | Difficulty {data['difficulty']}")
       
        if data['day_fish']:
            # This logic correctly formats the fish names for display.
            day_fish_display = sorted(list(set([f.replace('_', ' ') for f in data['day_fish']])))
            print(f"   - Day Fish: {', '.join(day_fish_display)}")

        if data['night_fish']:
            night_fish_display = sorted(list(set([f.replace('_', ' ') for f in data['night_fish']])))
            print(f"   - Night Fish: {', '.join(night_fish_display)}")


def admin_set_level(new_level_str):
    """Sets the player's level and resets their XP to 0 for that level."""
    global game_state
   
    try:
        # 1. Convert the argument to an integer
        new_level = int(new_level_str)
       
        # 2. Basic validation
        if new_level < 1:
            print("Level must be 1 or higher.")
            return

        # 3. Apply the cheat: Set level and reset XP
        game_state["level"] = new_level
        game_state["xp"] = 0
       
        print(f"\n*** CHEAT ACTIVATED: Level set to {new_level} (XP reset to 0)! ***")
       
    except ValueError:
        print("Admin Error: Level must be a whole number.")

# --- Main Game Loop ---
def main():
    print("=" * 70)
    print("         WELCOME TO FISHING SIMULATOR (Update 3.5)")
    print(f"    {len(locations)} LOCATIONS | {len(rod_upgrades_w1) + len(rod_upgrades_w2)} RODS | {len(fish_data)} FISH SPECIES")
    print("=" * 70)
    print("Objective: Catch fish, sell them, upgrade, and unlock new worlds!")
    # NOTE: secret code = code: gimme 'rod' for cheats, same with 'admin w2' also 'admin level number'
    print("Type 'help' for a list of commands. (code: immeg 'dro' ofr ceaths msae tiwh 'mdain 2w' lsao 'mdain leelv nubmre' )")

    while True:
        try:
            user_input = input(f"\n(W{game_state['world']} | {game_state['time_of_day'].upper()} at {game_state['location']}) > ").lower().split()
            if not user_input:
                continue

            command = user_input[0]
            args = user_input[1:]
           
# ... inside the main function's while loop ...

            # --- ADMIN COMMAND CHECKS ---
            if command == "admin" and args:
                if args[0] == "w2":
                    admin_skip_w2()
                    continue
                # --- START OF LEVEL CHEAT INSERTION ---
                elif args[0] == "level" and len(args) > 1:
                    admin_set_level(args[1])
                    continue
                # --- END OF LEVEL CHEAT INSERTION ---

# ... rest of your code ...
            # --- NEW ROD CHEAT CODE ---
            if command == "gimme" and len(args) > 1 and args[0] == "rod":
                rod_key_args = args[1:]
                rod_key = "_".join(rod_key_args) # e.g., 'little_teddy_rod'
                admin_get_rod(rod_key)
                continue
            # --------------------------

            if command in ["fish", "f"]:
                start_fishing()
            elif command in ["shop", "s"]:
                go_shop()
            elif command == "go":
                if not args: print("Usage: go <location> (e.g., go ocean coast)")
                else: change_location(args)
            elif command == "bait":
                if not args: print("Usage: bait <type> (e.g., bait power bait)")
                else: change_bait(args)
            elif command in ["status", "i"]:
                print_status()
            elif command == "locations":
                print_locations()
            elif command == "craft":
                if not args: print("Usage: craft <rod name> (e.g., craft beary rod) (info: put i to see rods)")
                else: craft_rod(args)
            elif command == "help":
                print_help()
            elif command == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Unknown command. Type 'help'.")
       
        # FIX: Added a general exception handler to prevent the game from crashing.
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")
            print("Please try a different command.")

if __name__ == "__main__":
    main()
