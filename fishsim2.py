import random
import time

# --- Game State Variables ---
game_state = {
    "location": "Pond",
    "money": 100,
    "xp": 0,
    "level": 1,
    "current_bait": "worm",
    "rod_power": 1.0,  # Must be a float for correct multiplication
    "time_of_day": "day",
    "unlocked_locations": {"Pond"},  # Tracks locations you've paid the one-time fee for
    "day" : 1,
    "days_fished": 0,
    "total_fish_attempts": 0
}

# Inventory stores individual fish objects
inventory = []

# Bait stock initialisation
bait_stock = {
    "worm": 10,
    "cricket": 0,
    "minnow": 0,
    "lure": 0,
    "glow_worm": 0,
    # Specialized baits
    "deep_blob": 0,     # specialized for Deep Sea & Deep areas
    "tropical_powder": 0,  # specialized for Tropical Lagoon
    "ice_shrimp": 0     # specialized for Arctic Ice Shelf
}

# --- Data Tables ---

bait_data = {
    "worm": {"cost": 1, "catch_rate": 0.6, "night_bonus": 1.0},
    "cricket": {"cost": 3, "catch_rate": 0.75, "night_bonus": 1.0},
    "minnow": {"cost": 8, "catch_rate": 0.9, "night_bonus": 1.0},
    "lure": {"cost": 25, "catch_rate": 0.8, "night_bonus": 1.0},
    "glow_worm": {"cost": 10, "catch_rate": 0.7, "night_bonus": 1.5},
    # Specialized baits:
    "deep_blob": {"cost": 60, "catch_rate": 0.95, "night_bonus": 1.2},
    "tropical_powder": {"cost": 20, "catch_rate": 0.85, "night_bonus": 1.0},
    "ice_shrimp": {"cost": 30, "catch_rate": 0.88, "night_bonus": 1.1},
}

locations = {
    "Pond": {
        "access_cost": 0, "level_req": 1, "difficulty": 1,
        # Rarity: Minnows (5x) > Perch and Sunfish (3x and 2x) > Shiners/Catfish (1x)
        "day_fish": [
            "minnows", "minnows", "minnows", "minnows", "minnows",
            "perch", "perch", "perch",
            "sunfish", "sunfish",
            "shiners",
            "catfish",
        ],
        # Night Rarity: Catfish (1x) > Eel (4x) > Lanternfish (5x)
        "night_fish": [
            "lanternfish", "lanternfish", "lanternfish", "lanternfish", "lanternfish",
            "eel", "eel", "eel", "eel",
            "catfish",
        ]
    },
    "River": {
        "access_cost": 250, "level_req": 3, "difficulty": 3,
        # Rarity: Perch (5x) > Sunfish/Shiners (4x) > Catfish/Trout/Salmon (1x)
        "day_fish": [
            "perch", "perch", "perch", "perch", "perch",
            "sunfish", "sunfish", "sunfish", "sunfish",
            "shiners", "shiners", "shiners", "shiners"
            "catfish",
            "trout",
            "salmon",
        ],
        # Night Rarity: Catfish/Moonfish/Viperfish (1x) > Lanternfish (6x) > Eel (5x)
        "night_fish": [
            "lanternfish", "lanternfish", "lanternfish", "lanternfish", "lanternfish", "lanternfish",
            "eel", "eel", "eel", "eel", "eel",
            "catfish",
            "moonfish",
            "viperfish",
        ]
    },
    "Lake": {
        "access_cost": 750, "level_req": 7, "difficulty": 5,
        # Rarity: Trout/Salmon/Bass (1x) > Catfish (5x)
        "day_fish": [
            "catfish", "catfish", "catfish", "catfish", "catfish", "catfish",
            "trout",
            "salmon",
            "bass",
        ],
        # Night Rarity: Eel (8x) > Bass/Moonfish/Stargazer (1x) > Viperfish (2x)
        "night_fish": [
            "eel", "eel", "eel", "eel", "eel", "eel", "eel", "eel",
            "bass",
            "moonfish",
            "viperfish", "viperfish",
            "stargazer",
        ]
    },
    "Tropical Lagoon": {
        "access_cost": 2000, "level_req": 8, "difficulty": 7,
        # Rarity: Parrotfish (7x) > Dolphin/Dorado/Manta Ray (1x) > Clown_snapper (2x)
        "day_fish": [
            "parrotfish", "parrotfish", "parrotfish", "parrotfish", "parrotfish", "parrotfish", "parrotfish"
            "clown_snapper", "clown_snapper",
            "dolphin_fish",
            "dorado",
            "manta_ray",
        ],
        # Night Rarity: Parrotfish (5x) > Dorado/Reef_Shark (1x) > Moonfish (3x)
        "night_fish": [
            "parrotfish", "parrotfish", "parrotfish", "parrotfish", "parrotfish",
            "dorado",
            "moonfish", "moonfish" "moonfish",
            "reef_shark",
        ]
    },
    "Ocean Coast": {
        "access_cost": 5000, "level_req": 12, "difficulty": 8,
        # Rarity: Mackerel (7x) > Bluefish/Snapper/Dolphin/Dorado/Tuna (1x)
        "day_fish": [
            "mackerel", "mackerel", "mackerel", "mackerel", "mackerel", "mackerel", "mackerel",
            "bluefish",
            "snapper",
            "dolphin_fish",
            "dorado",
            "tuna",
        ],
        # Night Rarity: Eel (7x) > Shark/Moonfish/Viperfish/Shark/Swordfish (1x)
        "night_fish": [
            "eel", "eel", "eel", "eel", "eel", "eel", "eel",
            "moonfish",
            "viperfish",
            "shark",
            "swordfish",
        ]
    },
    "Deep Sea Trench": {
        "access_cost": 15000, "level_req": 20, "difficulty": 12,
        # Rarity: Angler (7x) > Giant Grouper/Colossal Squid (1x) > Oarfish (2x)
        "day_fish": [
            "anglerfish", "anglerfish", "anglerfish", "anglerfish", "anglerfish", "anglerfish", "anglerfish",
            "oarfish", "oarfish",
            "giant_grouper",
            "colossal_squid",
        ],
        # Night Rarity: Angler/Viper/Grouper/Colossal_Squid (1x) > Vampire Squid (5x)
        "night_fish": [
            "anglerfish",
            "viperfish",
            "giant_grouper",
            "colossal_squid",
            "vampire_squid", "vampire_squid", "vampire_squid", "vampire_squid", "vampire_squid",
        ]
    },
    "Arctic Ice Shelf": {
        "access_cost": 35000,
        "level_req": 25,
        "difficulty": 15,
        # Rarity: Polar Cod (4x) > Ice Cod/Arctic Chub (1x)
        "day_fish": [
            "polar_cod", "polar_cod", "polar_cod", "polar_cod",
            "ice_cod",
            "arctic_chub",
        ],
        # Night Rarity: Arctic Char (5x) > Seal/Penguin/Ice Shrimp/Killer_Whale (1x)
        "night_fish": [
            "arctic_char", "arctic_char", "arctic_char", "arctic_char", "arctic_char",
            "seal",
            "penguin",
            "ice_shrimp",
            "killer_whale",
        ]
    },
    "Volcanic Hotspot": {
        "access_cost": 80000, "level_req": 35, "difficulty": 18,
        # Rarity: Thermal Trout (5x) > Lava Eel/Fire Bass (2x) > Magma Shark (1x)
        "day_fish": [
            "thermal_trout", "thermal_trout", "thermal_trout", "thermal trout", "thermal trout",
            "lava_eel", "lava_eel",
            "fire_bass", "fire_bass",
            "magma_shark",
        ],
        # Night Rarity: Lava Eel/Pyro Snapper (5x) > Magma Shark/Obsidian Fish (1x)
        "night_fish": [
            "lava_eel", "lava_eel", "lava eel", "lava_eel", "lava_eel",
            "pyro_snapper", "pyro_snapper", "pyro_snapper", "pyro_snapper", "pyro_snapper",
            "magma_shark",
            "obsidian_fish",
        ]
    },
    "Subterranean Cave": {
        "access_cost": 250000, "level_req": 50, "difficulty": 25,
        # Rarity: Tetra (9x - as 'trash' catch) > Tiger Shark/Grouper/Abyssal Eel (1x - VERY RARE)
        "day_fish": [
            "tetra", "tetra", "tetra", "tetra", "tetra", "tetra", "tetra", "tetra", "tetra",
            "tiger_shark",
            "goliath_grouper",
            "abyssal_eel",
        ],
        # Night Rarity: Isopod (6x) > Tetra/Black Bream/Goliath Grouper (1x - VERY RARE)
        "night_fish": [
            "isopod", "isopod", "isopod", "isopod", "isopod", "isopod",
            "tetra",
            "black_bream",
            "goliath_grouper",
        ]
    }
}

fish_data = {
    # Pond/River/Lake Species (existing)
    "minnows": {"base_value": 3, "min_weight": 0.1, "max_weight": 0.5, "xp_per_lb": 1},
    "perch": {"base_value": 5, "min_weight": 0.2, "max_weight": 0.8, "xp_per_lb": 3},
    "shiners": {"base_value": 7, "min_weight": 0.3, "max_weight": 1.0, "xp_per_lb": 8},
    "lanternfish": {"base_value": 8, "min_weight": 0.4, "max_weight": 1.5, "xp_per_lb": 9},
    "eel": {"base_value": 10, "min_weight": 0.5, "max_weight": 3.0, "xp_per_lb": 10},
    "sunfish": {"base_value": 12, "min_weight": 0.5, "max_weight": 2.0, "xp_per_lb": 10},
    "catfish": {"base_value": 15, "min_weight": 1.0, "max_weight": 5.0, "xp_per_lb": 12},
    "trout": {"base_value": 25, "min_weight": 2.0, "max_weight": 8.0, "xp_per_lb": 18},
    "viperfish": {"base_value": 30, "min_weight": 3.0, "max_weight": 9.0, "xp_per_lb": 20},
    "moonfish": {"base_value": 35, "min_weight": 4.0, "max_weight": 12.0, "xp_per_lb": 22},
    "bass": {"base_value": 40, "min_weight": 3.0, "max_weight": 10.0, "xp_per_lb": 25},
    "salmon": {"base_value": 50, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 27},
    "stargazer": {"base_value": 60, "min_weight": 6.0, "max_weight": 18.0, "xp_per_lb": 29},

    # Ocean Coast Species (existing)
    "mackerel": {"base_value": 18, "min_weight": 1.5, "max_weight": 6.0, "xp_per_lb": 15},
    "bluefish": {"base_value": 38, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 25},
    "snapper": {"base_value": 45, "min_weight": 7.0, "max_weight": 20.0, "xp_per_lb": 30},
    "dolphin_fish": {"base_value": 55, "min_weight": 10.0, "max_weight": 30.0, "xp_per_lb": 15},
    "dorado": {"base_value": 65, "min_weight": 12.0, "max_weight": 40.0, "xp_per_lb": 32},
    "tuna": {"base_value": 80, "min_weight": 20.0, "max_weight": 50.0, "xp_per_lb": 34},
    "shark": {"base_value": 75, "min_weight": 30.0, "max_weight": 60.0, "xp_per_lb": 36},
    "swordfish": {"base_value": 100, "min_weight": 50.0, "max_weight": 80.0, "xp_per_lb": 37},

    # Deep Sea Trench Species (existing)
    "anglerfish": {"base_value": 150, "min_weight": 100.0, "max_weight": 150.0, "xp_per_lb": 32},
    "oarfish": {"base_value": 120, "min_weight": 80.0, "max_weight": 200.0, "xp_per_lb": 44},
    "giant_grouper": {"base_value": 200, "min_weight": 150.0, "max_weight": 300.0, "xp_per_lb": 0.2},
    "colossal_squid": {"base_value": 180, "min_weight": 200.0, "max_weight": 400.0, "xp_per_lb": 0.3},
    "vampire_squid": {"base_value": 50, "min_weight": 5.0, "max_weight": 10.0, "xp_per_lb": 2},

    # Tropical Lagoon (new species)
    "parrotfish": {"base_value": 28, "min_weight": 4.0, "max_weight": 12.0, "xp_per_lb": 22},
    "clown_snapper": {"base_value": 40, "min_weight": 6.0, "max_weight": 25.0, "xp_per_lb": 30},
    "manta_ray": {"base_value": 220, "min_weight": 60.0, "max_weight": 180.0, "xp_per_lb": 32},
    "reef_shark": {"base_value": 90, "min_weight": 25.0, "max_weight": 80.0, "xp_per_lb": 35},

    # Arctic Ice Shelf (new species)
    "polar_cod": {"base_value": 22, "min_weight": 2.0, "max_weight": 203.0, "xp_per_lb": 9},
    "ice_cod": {"base_value": 35, "min_weight": 5.0, "max_weight": 603.0, "xp_per_lb": 12},
    "arctic_chub": {"base_value": 45, "min_weight": 50.0, "max_weight": 700.0, "xp_per_lb": 0.1},
    "arctic_char": {"base_value": 65, "min_weight": 10.0, "max_weight": 50.0, "xp_per_lb": 9},
    "seal": {"base_value": 150, "min_weight": 200.0, "max_weight": 500.0, "xp_per_lb": 4},
    "penguin": {"base_value": 80, "min_weight": 5.0, "max_weight": 15.0, "xp_per_lb": 4},
    "killer_whale": {"base_value": 500, "min_weight": 500.0, "max_weight": 1000.0, "xp_per_lb": 0.1},

    # Volcanic Hotspot Species (new)
    "thermal_trout": {"base_value": 70, "min_weight": 5.0, "max_weight": 25.0, "xp_per_lb": 4},
    "lava_eel": {"base_value": 110, "min_weight": 15.0, "max_weight": 50.0, "xp_per_lb": 12},
    "fire_bass": {"base_value": 140, "min_weight": 20.0, "max_weight": 60.0, "xp_per_lb": 1},
    "magma_shark": {"base_value": 250, "min_weight": 100.0, "max_weight": 350.0, "xp_per_lb": 0.05},
    "pyro_snapper": {"base_value": 170, "min_weight": 25.0, "max_weight": 80.0, "xp_per_lb": 1},
    "obsidian_fish": {"base_value": 400, "min_weight": 400.0, "max_weight": 700.0, "xp_per_lb": 0.02},

    # Subterranean Cave Species (new)
    "tetra": {"base_value": 90, "min_weight": 1.0, "max_weight": 5.0, "xp_per_lb": 2},
    "tiger_shark": {"base_value": 350, "min_weight": 300.0, "max_weight": 800.0, "xp_per_lb": 0.05},
    "goliath_grouper": {"base_value": 550, "min_weight": 600.0, "max_weight": 1200.0, "xp_per_lb": 0.05},
    "abyssal_eel": {"base_value": 800, "min_weight": 1000.0, "max_weight": 2000.0, "xp_per_lb": 0.01},
    "isopod": {"base_value": 100, "min_weight": 0.5, "max_weight": 2.0, "xp_per_lb": 2},
    "black_bream": {"base_value": 150, "min_weight": 100.0, "max_weight": 150.0, "xp_per_lb": 0.5},
  }



rod_upgrades = {
    2: {"name": "Fiberglass Rod", "cost": 150, "rod_power": 1.5, "level_req": 2},
    3: {"name": "Graphite Rod", "cost": 400, "rod_power": 2.0, "level_req": 5},
    4: {"name": "Titanium Rod", "cost": 1500, "rod_power": 3.0, "level_req": 9},
    5: {"name": "Carbon Fiber Rod", "cost": 4500, "rod_power": 4.0, "level_req": 14},
    # Rods above are needed after lake
    6: {"name": "Electric Reel", "cost": 12000, "rod_power": 5.0, "level_req": 18},
    7: {"name": "Hydro-Drive Reel", "cost": 40000, "rod_power": 6.5, "level_req": 22},
    8: {"name": "Quantum Reel", "cost": 120000, "rod_power": 7.5, "level_req": 30},
    9: {"name": "Lightning Rod", "cost": 500000, "rod_power": 8.0, "level_req": 50},
    10: {"name": "Zapper Rod", "cost": 750000, "rod_power": 9.0, "level_req": 75},
    11: {"name": "Jotham's Rod", "cost": 1500000, "rod_power": 10.0, "level_req": 125},
    12: {"name": "Jerome's Rod", "cost": 2500000, "rod_power": 15.0, "level_req": 150},
    13: {"name": "Jairus's Reel", "cost": 7500000, "rod_power": 16.0, "level_req": 175},
    15: {"name": "Jairus's Proper Reel", "cost": 5000000, "rod_power": 20.0, "level_req": 200},
}

# --- Core Mechanics ---

def toggle_time_of_day():
    """switches between day n night"""
    if game_state["time_of_day"] == "day":
        game_state["time_of_day"] = "night"
        print("\n*** the sun sets, and it is now NIGHT ***")
    else:
        game_state["time_of_day"] = "day"
        game_state["day"] += 1   # only goes up when it's day
        print(f"\n*** the sun rises — it’s now DAY {game_state['day']}! ***")


def check_level_up():
    """Checks and applies level-up logic based on XP."""
    while game_state["xp"] >= game_state["level"] * 50:
        game_state["xp"] -= game_state["level"] * 50
        game_state["level"] += 1
        print(f"\n*** LEVEL UP! You are now Level {game_state['level']}! ***")
        print("Your reeling skill has improved — fish struggle less against you!")

def calculate_catch():
    """Determines if a fish is caught, and if so, what kind and how big."""
    # 1. Determine available fish pool based on time of day
    if game_state["time_of_day"] == "day":
        possible_fish = locations[game_state["location"]]["day_fish"]
    else:
        possible_fish = locations[game_state["location"]]["night_fish"]

    # 2. Calculate Catch Chance (Bait specific logic added)
    base_rate = bait_data[game_state["current_bait"]]["catch_rate"]

    # Apply night bonus if using glow worm at night (and other baits with night bonuses)
    if game_state["time_of_day"] == "night":
        base_rate *= bait_data[game_state["current_bait"]].get("night_bonus", 1.0)

    # Difficulty modifier: higher difficulty reduces success; higher level increases chance
    difficulty_mod = locations[game_state["location"]]["difficulty"] / max(1, game_state["level"])
    catch_chance = base_rate * (1 + (1 - difficulty_mod) * 0.1)

    # Clamp catch_chance to reasonable bounds, ensuring it is between 2% and 100%
    catch_chance = max(0.02, min(1.0, catch_chance))

    if random.random() > catch_chance:
        print("...nothing but seaweed. The fish aren't biting.")
        return None

    # 3. Select the fish type and calculate weight
    # This line now relies on the list duplication in the 'locations' dictionary for rarity.
    fish_name = random.choice(possible_fish)
    data = fish_data[fish_name]

    max_w = data["max_weight"] * game_state["rod_power"]

    # Ensure min_weight is not larger than max_w
    min_w = data["min_weight"]
    if min_w > max_w:
        min_w = max_w / 2  # Fallback to prevent error

    weight = round(random.uniform(min_w, max_w), 2)

    # Calculate selling value based on exact weight
    base_value = data["base_value"]
    selling_value = int(base_value * weight * random.uniform(0.9, 1.1))  # marketplace fluctuation

    return {"type": fish_name, "weight": weight, "value": selling_value}

def start_fishing():
    """Simulates the fishing process, including reeling mini-game enhanced with level multiplier."""
    game_state["total_fish_attempts"] += 1
    if bait_stock[game_state["current_bait"]] <= 0:
        print(f"You are out of {game_state['current_bait']}! Change bait or buy more.")
        return

    # Bait is used up upon casting
    bait_stock[game_state["current_bait"]] -= 1


    print(f"Casting line with {game_state['current_bait']} at the {game_state['location']} during {game_state['time_of_day']}...")
    time.sleep(1)

    # Level increases the bite time speed (faster bites at higher levels)
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

    # --- Reeling Mini-Game ---
    print(f"\n!!! FISH ON! It feels like a {fish_name.upper()} of {weight} lbs! Estimated value: ${selling_value}! !!!")

    # Reeling difficulty base: weight * location difficulty divided by rod power
    base_reeling_difficulty = weight * locations[game_state["location"]]["difficulty"] / max(0.0001, game_state["rod_power"])

    # Level Multiplier (CRITICAL FIX)
    # Higher level reduces the effective struggle of the fish.
    # Design: level_effect = 1 + (level - 1) * 0.05 -> each level gives 5% extra leverage, cap at 25.0.
    # Final fish struggle is divided by this level_effect, so higher level -> lower struggle.
    level_effect = 1.0 + (game_state["level"] - 1) * 0.05
    level_effect = min(level_effect, 25.0)  # cap to prevent absurd division

    reeling_difficulty = base_reeling_difficulty / level_effect

    # Reeling goal
    success_bar = 0
    max_bar = 100

    input("Press ENTER to start reeling!")

    start_time = time.time()

    # 10 second limit for the fight
    while success_bar < max_bar and time.time() - start_time < 10:

        # Player reeling (multiplied by rod power). Make it integer-ish for readability.
        player_reels = random.randint(10, 20) * game_state["rod_power"]
        success_bar += player_reels

        # Fish struggles: reduce by level_effect indirectly already applied in reeling_difficulty.
        # Ensure the randint bounds are valid and reasonable even for small values.
        low_bound = max(1, int(reeling_difficulty / 2))
        high_bound = max(low_bound, int(reeling_difficulty))
        fish_struggle = random.randint(low_bound, high_bound)

        # As a final safeguard, reduce fish_struggle further by a small factor based on rod_power
        # (higher-power rods help calm the fish).
        rod_effect = 1.0 + (game_state["rod_power"] - 1.0) * 0.1
        fish_struggle = int(fish_struggle / rod_effect)

       # Decrease the success bar by the fish struggle
        success_bar -= fish_struggle

        # CAP: Ensure the success_bar is between 0 and max_bar (100)
        success_bar = max(0, min(max_bar, success_bar))

        # Use a consistent bar width for cleaner output
        bar_width = 20
        filled = int(success_bar * bar_width / max_bar)
        bar = '█' * filled + '░' * (bar_width - filled)

        print(f"  > Reeling... [{bar}] {int(success_bar)}/{max_bar} | Struggle: -{fish_struggle} (LvlEff:{level_effect:.2f})")
        time.sleep(0.5)

    # --- Reeling Result ---
    if success_bar >= max_bar:
        xp_gained = int(weight * fish_data[fish_name]["xp_per_lb"])
        inventory.append(catch_result)  # Store the fish object
        game_state["xp"] += xp_gained
        print(f"\nSuccess! You landed a {weight} lb {fish_name.title().replace('_', ' ')}!")
        print(f"Gained {xp_gained} XP!")
        check_level_up()
    else:
        print("\nOh no! The line snapped and the fish got away.")

    toggle_time_of_day()  # Toggle time after the attempt
    game_state["days_fished"] += 1
# --- Shop and Inventory ---

def go_shop():
    """Opens the tackle shop for buying bait and upgrades."""
    global game_state

    while True:
        print("\n--- TACKLE SHOP ---")
        print(f"Money: ${game_state['money']} | Level: {game_state['level']} | Rod Power: {game_state['rod_power']}")
        print("[1] Buy Bait")
        print("[2] Sell Catch")
        print("[3] Buy Rod Upgrades")
        print("[0] Exit Shop")
        choice = input("> ")

        if choice == "1":
            print("\n--- Buy Bait ---")
            for i, (bait_name, data) in enumerate(bait_data.items(), 1):
                notes = ""
                if "night_bonus" in data and data["night_bonus"] > 1.0:
                    notes = (notes + " (Night catch bonus!)").strip()
                print(f" [{i}] {bait_name.title().replace('_', ' ')} (Cost: ${data['cost']} per unit) Stock: {bait_stock[bait_name]}{notes}")

            try:
                bait_choice = int(input("Select bait (1-{}): ".format(len(bait_data))))
                bait_list = list(bait_data.keys())
                bait_name = bait_list[bait_choice - 1]
                cost = bait_data[bait_name]["cost"]

                amount = int(input(f"How many {bait_name} to buy? (Max: {game_state['money'] // cost}): "))
                total_cost = amount * cost

                if total_cost > game_state["money"]:
                    print("Not enough money!")
                elif amount > 0:
                    game_state["money"] -= total_cost
                    bait_stock[bait_name] += amount
                    print(f"Bought {amount} {bait_name} for ${total_cost}. Stock: {bait_stock[bait_name]}")
                else:
                    print("Invalid amount.")
            except (ValueError, IndexError):
                print("Invalid input.")

        elif choice == "2":
            if not inventory:
                print("Your cooler is empty. No fish to sell.")
                continue

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

        elif choice == "3":
            print("\n--- Buy Rod Upgrades ---")

            upgrade_options = []
            for tier, data in rod_upgrades.items():
                if data["rod_power"] > game_state["rod_power"]:
                    upgrade_options.append(data)

            if not upgrade_options:
                print("You already own the highest available rod.")
                continue

            for i, data in enumerate(upgrade_options, 1):
                print(f" [{i}] {data['name']} (Power: {data['rod_power']} | Cost: ${data['cost']} | Level Req: {data['level_req']})")

            try:
                upgrade_choice = input("Enter the number of the next upgrade or 0 to back: ")
                if upgrade_choice == "0":
                    continue

                selected_upgrade = upgrade_options[int(upgrade_choice) - 1]

                if game_state["level"] < selected_upgrade["level_req"]:
                    print(f"You need to be Level {selected_upgrade['level_req']} to buy this rod.")
                elif game_state["money"] < selected_upgrade["cost"]:
                    print(f"You need ${selected_upgrade['cost']} to buy the {selected_upgrade['name']}.")
                else:
                    game_state["money"] -= selected_upgrade["cost"]
                    game_state["rod_power"] = selected_upgrade["rod_power"]
                    print(f"Purchased {selected_upgrade['name']}! Rod Power is now {game_state['rod_power']}.")
            except (ValueError, IndexError):
                print("Invalid input.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def change_location(new_location):
    """Allows the player to move between fishing spots with a one-time fee."""
    # Standardize multi-word input
    new_location_key = " ".join(new_location).title()

    if new_location_key not in locations:
        print("Unknown location. Available:", ", ".join(locations.keys()))
        return

    data = locations[new_location_key]

    if new_location_key == game_state["location"]:
        print(f"You are already at the {new_location_key}.")
        return

    # Check Level Requirement
    if game_state["level"] < data["level_req"]:
        print(f"You must be Level {data['level_req']} to travel to the {new_location_key}.")
        return

    # --- LOGIC FOR ONE-TIME FEE ---
    if new_location_key in game_state["unlocked_locations"]:
        # If unlocked, travel is free
        game_state["location"] = new_location_key
        print(f"Traveled to the {new_location_key}. Access is FREE! (Location already unlocked).")
    else:
        # If not unlocked, charge the access cost
        if game_state["money"] < data["access_cost"]:
            print(f"You need ${data['access_cost']} to unlock the {new_location_key}.")
            return

        game_state["money"] -= data["access_cost"]
        game_state["location"] = new_location_key
        game_state["unlocked_locations"].add(new_location_key)  # Mark as unlocked
        print(f"Purchased access to the {new_location_key}!")
        print(f"Access fee: ${data['access_cost']} deducted. This location is now permanently unlocked for free travel!")

    print(f"You can now catch day fish: {', '.join(data['day_fish']).replace('_', ' ')} and night fish: {', '.join(data['night_fish']).replace('_', ' ')}.")

def change_bait(new_bait):
    """Switches the current bait if the player has it in stock."""
    new_bait_key = "_".join(new_bait)

    if new_bait_key not in bait_data:
        print("Unknown bait. Available:", ", ".join(bait_data.keys()))
        return

    if bait_stock[new_bait_key] <= 0:
        print(f"You are out of {new_bait_key.title().replace('_', ' ')}. Visit the shop to buy more.")
        return

    game_state["current_bait"] = new_bait_key
    print(f"Switched bait to {new_bait_key.title().replace('_', ' ')}.")

# --- UI and Helper Functions ---

def print_status():
    """Displays the player's current stats and inventory."""
    print("\n--- ANGLER STATUS ---")
    print(f"Time of Day: {game_state['time_of_day'].upper()}")
    print(f"Day {game_state['day']} | Time: {game_state['time_of_day'].title()} | Days Fished: {game_state['days_fished']}")
    print(f"Location: {game_state['location']} (Difficulty {locations[game_state['location']]['difficulty']})")
    print(f"Money: ${game_state['money']}")
    print(f"Level: {game_state['level']} (XP: {game_state['xp']}/{game_state['level'] * 50})")
    print(f"Total Days Fished: {game_state['days_fished']} | Total Fish Tried: {game_state['total_fish_attempts']}")
    # Show the maximum available rod power from the highest rod upgrade
    max_available_power = max(v["rod_power"] for v in rod_upgrades.values())
    print(f"Rod Power: {game_state['rod_power']} (Max available: {max_available_power})")
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
    for bait, qty in bait_stock.items():
        if qty > 0:
            print(f" - {bait.title().replace('_', ' ')}: {qty}")

def print_help():
    """Shows all available commands."""
    print("\n--- Commands ---")
    print(" **fish / f** : Cast your line and try to catch a fish. **Toggles Day/Night.**")
    print(" **shop / s** : Go to the Tackle Shop to buy/sell/upgrade.")
    print(" **go <location>** : Travel to a new fishing spot (e.g., go ocean coast). Requires one-time Level/Money fee.")
    print(" **bait <type>** : Change your current bait (e.g., bait minnow).")
    print(" **status / i** : Show your money, level, inventory, and bait stock.")
    print(" **locations** : View all available fishing spots and costs/requirements.")
    print(" **help** : Show this list of commands.")

def print_locations():
    """Shows location information."""
    print("\n--- Fishing Locations (Requirements & Fish) ---")
    for name, data in locations.items():
        is_unlocked = "✅ UNLOCKED (Free Travel)" if name in game_state["unlocked_locations"] else f"❌ LOCKED (One-time Fee: ${data['access_cost']})"
        print(f" - {name}: {is_unlocked} | Level Req: {data['level_req']} | Difficulty {data['difficulty']}")
        print(f"   - Day Fish: {', '.join(data['day_fish']).replace('_', ' ')}")
        print(f"   - Night Fish: {', '.join(data['night_fish']).replace('_', ' ')}")

# --- Main Game Loop ---
print("=" * 70)
print("         WELCOME TO FISHING SIMULATOR")
print(f"    {len(locations)} LOCATIONS | {len(rod_upgrades)} RODS | {len(fish_data)} FISH SPECIES | PERMANENT TRAVEL")
print("=" * 70)
print("Objective: Catch fish, sell them for profit, upgrade your rod, and unlock new areas.")
print("Type 'help' for a list of commands.")

while True:
    try:
        user_input = input(f"\n({game_state['time_of_day'].upper()} at {game_state['location']}) > ").lower().split()
        if not user_input:
            continue

        command = user_input[0]
        args = user_input[1:]

        if command in ["fish", "f"]:
            start_fishing()
        elif command in ["shop", "s"]:
            go_shop()
        elif command == "go":
            if not args:
                print("Usage: go <location> (e.g., go ocean coast)")
            else:
                change_location(args)
        elif command == "bait":
            if not args:
                print("Usage: bait <type> (e.g., bait minnow)")
            else:
                change_bait(args)
        elif command in ["status", "i"]:
            print_status()
        elif command == "locations":
            print_locations()
        elif command == "help":
            print_help()
        else:
            print("Unknown command. Type 'help'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}. Check your input format.")
