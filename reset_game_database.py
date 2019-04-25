"""
This script starts a new game when you run it!

It clears all previous information, so don't run it unless you know what you're doing
"""
import constants
from database import Database

def create_default_monsters():
    """
    :return: list of default monsters
    """
    with open(constants.Database.MONSTER_PATH) as monster_file:
        monster_data = json.load(monster_file)
if __name__ == "__main__":
    # First ensure the database exists
    Database.create_game_object_tables()

    # Delete any tables if they already exist
    Database.delete_tables()

    # Populate database with default monsters
