import sys
sys.path.append('__HOME__/DEMMO')

# Whether or not we are print testing in non-test.py files (e.g. database.py)
TESTING = False
# Whether or not this is the server
IS_SERVER = True

PROJECT_HOME = '/var/jail/home/yanniw/DEMMO/' if IS_SERVER else ""

# Default player values
class Player:
    DEFAULT_HEALTH = 5
    DEFAULT_POWER = 5
    DEFAULT_GOLD = 0
    DEFAULT_BOSS_DEFEATED = 0

# Shop costs
class Shop:
    BASE_HEALTH_COST = 100
    BASE_POWER_COST = 100

# Database constants
class Database:
    TEST_GAME_DB = "test_game_info.db"
    GAME_DB = "game_info.db"
    TRUE = "True"
    FALSE = "False"

    # JSON files
    MAP_FILE = "map.json"
    TEST_MAP_FILE = "test_map.json"
    MONSTER_FILE = "monsters.json"

    # Directory paths
    # resources path based on server or local
    RESOURCES_DIR = PROJECT_HOME + "resources/"
    # database and map paths
    DATABASE_PATH = RESOURCES_DIR+GAME_DB
    MAP_PATH = RESOURCES_DIR+MAP_FILE
    MONSTER_PATH = RESOURCES_DIR+MONSTER_FILE

    # (Testing) Directory paths
    # resources path based on server or local
    TEST_RESOURCES_DIR = "test_resources/"
    # database and map paths
    TEST_DATABASE_PATH = TEST_RESOURCES_DIR+TEST_GAME_DB
    TEST_MAP_PATH = TEST_RESOURCES_DIR+TEST_MAP_FILE

# Game constants
class Game:
    class ServerMap:
        DIVIDER_MULTIPLIER = 4 # Determines size of the divider -> larger number = longer divider
        TILE_SIZE = 3 # size of each tile on the map
        ONLY_ID = False # whether or not to display only id of each player or monster
        TILE_INDENT = 1 # amount of indent for each tile


# TODO: Rename this
# Constant for within range functions
RANGE = 2 # number of tiles

# TODO: Add constants for player actions i.e. FIGHT = "FIGHT"