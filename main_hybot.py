import time
import requests
from datetime import datetime

key = str(input("What is your Hypixel API Key?"))
player_name = str(input("What is your Minecraft Username?"))
profile_choice = int(input("What profile do you want to track? (1 to 5, inclusive, in the order that they appear in the profile menu)")) - 1
coll_choice = str(input("What collection do you want to track?"))
skill_choice = str(input("What skill do you want to track?"))

''' # Possible Collections to Track: 
SUGAR_CANE
COBBLESTONE
COAL
REDSTONE
EMERALD
DIAMOND
OBSIDIAN
GOLD_INGOT
IRON_INGOT
MITHRIL_ORE
LOG
CACTUS
SAND
MELON
PUMPKIN
WHEAT
SEEDS
POTATO_ITEM
MUSHROOM_COLLECTION
HARD_STONE
GEMSTONE_COLLECTION
QUARTZ
GRAVEL
RAW_FISH
ICE
ENDER_PEARL
MAGMA_CREAM
GLOWSTONE_DUST
MAGMA_FISH
SAND
MYCEL
GLACITE
UMBER
TUNGSTEN
'''

''' # Possible Skills to Track:

mining
fishing
farming
foraging
combat

'''

### Credit: Bugfroggy and Chamos144

TStamp = int(time.time())  
TSTampOUT = str(TStamp)
print("Unix Timestamp: " + TSTampOUT)

UUIDGet = requests.get(
    "https://api.mojang.com/users/profiles/minecraft/" + player_name + "?at=" + TSTampOUT).json()  
uuid = str(UUIDGet["id"])


###

# not used (yet)
items = [
    "SLIME_BALL",
    "SUGAR_CANE",
    "COBBLESTONE",
    "COAL",
    "ROTTEN_FLESH",
    "REDSTONE",
    "EMERALD",
    "BONE",
    "DIAMOND",
    "OBSIDIAN",
    "GOLD_INGOT",
    "IRON_INGOT",
    "SULPHUR",
    "INK_SACK",
    "MITHRIL_ORE",
    "LOG",
    "LOG_2",
    "FEATHER",
    "RAW_CHICKEN",
    "CARROT_ITEM",
    "CACTUS",
    "SAND",
    "MUTTON",
    "RABBIT",
    "NETHER_STALK",
    "MELON",
    "PUMPKIN",
    "WHEAT",
    "SEEDS",
    "INK_SACK",
    "POTATO_ITEM",
    "MUSHROOM_COLLECTION",
    "INK_SACK",
    "HARD_STONE",
    "GEMSTONE_COLLECTION",
    "BLAZE_ROD",
    "QUARTZ",
    "STRING",
    "SPIDER_EYE",
    "LOG_2",
    "LOG",
    "LOG",
    "LOG",
    "GRAVEL",
    "RAW_FISH",
    "RAW_FISH",
    "WATER_LILY",
    "ICE",
    "CLAY_BALL",
    "PRISMARINE_CRYSTALS",
    "RAW_FISH",
    "SULPHUR_ORE",
    "SPONGE",
    "PRISMARINE_SHARD",
    "LEATHER",
    "RAW_FISH",
    "LOG",
    "ENDER_STONE",
    "ENDER_PEARL",
    "ENCHANTED_DIAMOND",
    "ENCHANTED_SLIME_BALL",
    "PORK",
    "MAGMA_CREAM",
    "GLOWSTONE_DUST",
    "GHAST_TEAR",
    "RABBIT_HIDE",
    "WOOL",
    "MAGMA_FISH",
    "SAND",
    "WILTED_BERBERIS",
    "CADUCOUS_STEM",
    "AGARICUS_CAP",
    "METAL_HEART",
    "HALF_EATEN_CARROT",
    "HEMOVIBE",
    "NETHERRACK",
    "MYCEL",
    "GLACITE",
    "UMBER",
    "TUNGSTEN",
    "TIMITE"
]

# Pulls profile from Hypixel API
player = requests.get(f"https://api.hypixel.net/player?key={key}&uuid={uuid}").json()
#print("profile id: " + list(player['player']['stats']['SkyBlock']['profiles'].keys())[profile_choice])
profile = list(player['player']['stats']['SkyBlock']['profiles'].keys())[profile_choice]
profile = f"{profile[0:8]}-{profile[8:12]}-{profile[12:16]}-{profile[16:20]}-{profile[20:32]}" # convert to required format

def update():
    return requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{player_name}").json()

def next_level_xp(c, n):
    if n == None:
        return "Skill Maxed!"
    else:
        return round(n - c, 2)
    
def calcTime(): # produces time in hours
    return (time.time() - TStamp) / 3600

    

# Main
def begin():
    p = update()
    start_coll = p['profiles'][profile]['raw']['collection'][coll_choice]
    start_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xp']
    prog_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpCurrent']
    next_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpForNext']
    
    while True:
        # updates player data 
        recent_coll = p['profiles'][profile]['raw']['collection'][coll_choice]
        recent_xp_amount = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xp']
        recent_prog_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpCurrent']
        recent_next_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpForNext']
        p = update()
        current_coll = p['profiles'][profile]['raw']['collection'][coll_choice]
        current_xp =  p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xp']
        current_prog_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpCurrent']
        current_next_xp = p['profiles'][profile]['data']['skills']['skills'][skill_choice]['xpForNext']

        print("======== REPORT =======")
 
        print(f"{coll_choice} for {player_name} at ",datetime.now(),": ",current_coll)
        print("Since start of program: ",current_coll - start_coll)
        print("Since Last request: ", current_coll - recent_coll)
        print(f"Amount of {skill_choice} xp for {player_name} at ",datetime.now(),": ",round(current_xp, 2))
        print(f"{skill_choice} XP earned since starting: ", round(current_xp - start_xp, 2))
        print(f"{skill_choice} XP earned since last update: ", round(current_xp - recent_xp_amount, 2))
        print(f"{skill_choice} XP required for next level:", next_level_xp(current_prog_xp, current_next_xp))
        print(f"Average {skill_choice} XP earned per hour:", round((current_xp - start_xp) / calcTime(), 2))
        print("")
 
        print("=======================")
 
        #Sleep for a reasonable time untill new API data is available (3-4 minutes)
        time.sleep(240)
begin() ### discord integration removed since bot is private, will release at a later date hopefully###
 