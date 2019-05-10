import sys
sys.path.append('__HOME__/DEMMO')
import constants
from containers.map import Map
from response_creator import ResponseCreator

class Game:
    """
    Class representing an on-going DEMMO game
    AF(map) = Game that contains a map, which stores tiles that contain player and monster
            objects
    """
    map_constants = constants.Game.ServerMap # alias for constants used for rendering the map of the game

    def __init__(self, rows, columns, players, monsters):
        """
        Initializes a new game object with players, monster, and a map of the game
        :param rows: (int) number of rows on the game map
        :param columns: (int) number of columns of the game map
        :param players: (list) players in the game
        :param monsters: (list) monsters in the game
        """
        self.id_to_players = {} # map of {player_id: player}
        self.id_to_monsters = {} # map of {monster_id: monster}
        self.map = Map(rows, columns) # a list of list of tiles
        # Populate the game map with players in the corresponding locations
        for player in players:
            self.add_player(player)

        # Populate the game map with monsters in the corresponding locations
        for monster in monsters:
            self.add_monster(monster)

    def add_player(self, player):
        """
        Adds a new player to the game
        :param player: (Player) to add to the game
        :return: None
        """
        player_id = player.id
        self.id_to_players[player_id] = player
        # Add player id to a tile
        row, col = player.get_location()
        tile = self.map.get_tile(row, col)
        tile.add_player(player_id)

    def add_monster(self, monster):
        """
        Add a new monster to the game
        :param monster: (Monster) to add to the game
        :return: None
        """
        monster_id = monster.id
        self.id_to_monsters[monster_id] = monster
        # Add monster id to a tile
        row, col = monster.get_location()
        tile = self.map.get_tile(row, col)
        tile.add_monster(monster_id)

    def get_player_stats(self, player_id):
        """
        Gets the stats of a selected player
        :param player_id: player to locate
        :return: stats of the player, including their health, power, luck, gold, and number of bosses defeated
        """
        player = self.id_to_players[player_id]
        return player.get_player_stats()

    def get_monster_stats(self, monster_id):
        """
        Gets the stats of a selected monster
        :param monster_id: monster to locate
        :return: stats of the monster, including their health, power, etc.
        """
        monster = self.id_to_monsters[monster_id]
        return monster.get_monster_stats()

    def has_player(self, player_id):
        """
        Returns whether the game has a specific player_id
        :param player_id: the player's id
        :return: True if the game has the player and False otherwise
        """
        return player_id in self.id_to_players

    def execute(self, **kwargs):
        """
        Executes a player action
        :param kwargs: (dict) contains player_id, action, and additional parameters that indicator the player's actions
        :return: a list of game objects that have changed from executing player action
        :raises ValueError: if a value from kwargs is invalid
        """
        action = kwargs['action']
        player_id = kwargs['player_id']
        player = self.id_to_players[player_id]

        changed_objects = []
        if action == constants.Game.DOWN:
            # Move down
            changed_objects.append(player.move_down())
        elif action == constants.Game.UP:
            # Move up
            changed_objects.append(player.move_up())
        elif action == constants.Game.LEFT:
            # Move left
            changed_objects.append(player.move_left())
        elif action == constants.Game.RIGHT:
            # Move right
            changed_objects.append(player.move_right())
        elif action == constants.Game.FIGHT_RESULT:
            health = kwargs['health']
            changed_objects.extend(self.process_fight_result(player, health))

        return changed_objects

    def process_fight_result(self, player, health):
        changed_objects = []
        player_id = player.id
        # Process result of a fight
        if health < 0:
            raise ValueError("Error: New player health is less than 0")
        elif health > player.get_health():
            raise ValueError("Error: New player health cannot be greater than before")
        player.health = health  # passed checks, update player health
        changed_objects.append(player)

        # Find the monster the player defeated and update it
        monster = self.get_monster_on_top_of_player(player_id)
        if monster is not None and monster.is_boss:
            monster.defeated_by.add(player_id)
            changed_objects.append(monster)
        return changed_objects

    def get_monster_on_top_of_player(self, player_id):
        """
        Returns the monster located in the same tile as the player if a monster exists, otherwise return None
        :param player_id: the id of the player
        :return: a monster object if a monster exists in the same tile as the player and None otherwise
        """
        player = self.id_to_players[player_id]
        row, col = player.get_location()
        tile = self.map.get_tile(row, col)
        if tile.has_monster():
            monster_id = tile.get_monster()
            monster = self.id_to_monsters[monster_id]
            # the player can only fight the monster if the monster is not a boss or if the player
            #   has not defeated the boss already
            if not monster.get_is_boss() \
                    or (monster.get_is_boss() and player_id not in monster.get_defeated_by()):
                return self.id_to_monsters[monster_id]
            else:
                return None
        return None

    def get_server_map(self):
        return ResponseCreator(self).get_server_map()

    def __str__(self):
        return self.get_server_map()


if __name__ == '__main__':
    # Run this code if testing is true, set to off otherwise! (real test cases are probably better :))
    if constants.TESTING:
        # Code for creating a dummy game and printing it
        from containers.player import Player
        from containers.monster import Monster
        rows = 5
        columns = 5
        players = [
            Player("Lucian", 0, 0),
            Player("Caitlyn", 1, 1),
            Player("Teemo", 2, 4),
            Player("Ze", 4, 2)
        ]
        monsters = [
            Monster("Baron", 0, 0, 9001, 200),
            Monster("Dragon", 1, 2, 1000, 100),
            Monster("Raptor", 4, 3, 100, 5)
        ]

        game = Game(rows, columns, players, monsters)
        print(game)