"""
This script resets the game database to only having default monsters when you run it!

It clears all previous information, so don't run it unless you know what you're doing
"""
import constants
import json
from containers.monster import Monster
from database import Database, Serialize

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

if __name__ == "__main__":
    print("Resetting game database...")
    # Delete any pre-existing tables to clear any previous monster or player information
    Database.delete_tables()
    # Now create empty tables in the database
    Database.create_game_object_tables()
    # Next, parse the monsters json file to create monster objects
    monsters = create_default_monsters()
    # Lastly, add the default monsters to the database
    Serialize.updateGameObjects(monsters)
    print("Done!")

