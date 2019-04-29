"""
This script resets the game database to only having default monsters when you run it!

It clears all previous information, so don't run it unless you know what you're doing
"""
import sys
sys.path.append('__HOME__/DEMMO')

import constants
import json
from containers.monster import Monster
from database import Database, Serialize

def resetDatabase():
    # Next, parse the monsters json file to create monster objects
    monsters = create_default_monsters()
    # Create empty tables in the database
    Database.create_game_object_tables()
    # Lastly, add the default monsters to the database
    Serialize.updateGameObjects(monsters)

def create_default_monsters():
    """
    :return: list of default monsters
    """
    with open(constants.Database.MONSTER_PATH) as monster_file:
        monster_data = json.load(monster_file)

        monsters = []
        for monster_info in monster_data['monsters']:
            id = monster_info['id']
            row = monster_info['row']
            col = monster_info['col']
            health = monster_info['health']
            power = monster_info['power']
            is_boss = monster_info['is_boss']
            defeated_by = set(monster_info['defeated_by'])
            monsters.append(Monster(id, row, col, health, power, is_boss, defeated_by))

        return monsters

def request_handler(request=None):
    """
    Returns the game database with default monsters and no players
    :param request: not used
    :return: (string) indicating success
    """
    Database.delete_tables()
    resetDatabase()
    return "Reset database successful"

if __name__ == "__main__":
    if not constants.IS_SERVER:
        print("Resetting game database...")
        # LOCAL only
        # Delete any pre-existing tables to clear any previous monster or player information
        Database.delete_tables()
        resetDatabase()

        print("Done!")

