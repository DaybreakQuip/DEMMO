import sys
sys.path.append('__HOME__/DEMMO')

import constants



class Map:
    """
    Class representing the map of the game with tiles at each square in the grid
    """
    def __init__(self, rows, columns):
        """
        Initializes a new Map object
        :param rows: (int) number of rows on the map
        :param columns: (int) number of columns on the map
        """
        self.rows = rows
        self.columns = columns
        self.tiles = [[Tile() for _ in range(columns)] for _ in range(rows)]

    def number_to_coords(self, tile_number):
        """
        Converts from a grid number to (row, col) format
        :param tile_number: (int) number of the grid, must be 0 <= tile_number < rows * columns
        :return: (tuple) of (row, col) of the converted grid number
        """
        if tile_number < 0 or tile_number >= self.rows * self.columns:
            raise ValueError("tile_number is < 0 or >= rows * columns: {}".format(tile_number))

        row = tile_number // self.columns
        col = tile_number % self.columns
        return (row, col)
    
    def coords_to_number(self, row, col):
        """
        converst from (row, col) to a grid number
        :param row: (int) current row, 0 <= row < rows
        :param col: (int) current col, 0 <= col < cols
        :return: (int) representing the grid number
        """
        width = self.columns # number of columns = width of the map
        return row * width + col
    
    def get_number_of_tiles(self):
        return self.rows * self.columns

    def get_tile(self, row, col):
        return self.tiles[row][col]

class Tile:
    """
    Class representing a single tile, which can be populated by players and/or monsters
    """
    def __init__(self):
        """
        Creates a new tile that contains a list of players and monsters i
        """
        self.players = set() # set of player ids
        self.monsters = set() # set of monster ids

    def has_player(self, player_id):
        return player_id in self.players

    def has_monster(self, monster_id):
        return monster_id in self.monsters

    def add_player(self, player_id):
        self.players.add(player_id)

    def remove_player(self, player_id):
        self.players.remove(player_id)

    def add_monster(self, monster_id):
        self.monsters.add(monster_id)

    def remove_monster(self, monster_id):
        self.monsters.remove(monster_id)
    
    def is_empty(self):
        return not(self.players or self.monsters)

    def __str__(self, base_indent=0, only_id=False):
        """
        Returns a string representation of a Tile object
        :param base_indent: (int) base indent level for the string
        :param only_id: (bool) indicating whether only the id of the game object will be shown
        :return: (string) string rep of the tile
        """
        indent = '\t' * base_indent
        temp_list = [] # temporary list to hold the string representation of the tile
        # Add all the players to the string
        if self.players:
            temp_list.append(indent + "Player(s):\n")
            for player in self.players:
                temp_list.append(indent + "\t{}\n".format(player))
        # Add all the monsters to the string
        if self.monsters:
            temp_list.append(indent + "Monster(s):\n")
            for monster in self.monsters:
                temp_list.append(indent + "\t{}\n".format(monster))
        return ''.join(temp_list)
        

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
            player_id = player.id
            self.id_to_players[player_id] = player
            # Add player id to a tile
            row, col = player.getLocation()
            tile = self.map.get_tile(row, col)
            tile.add_player(player_id)

        # Populate the game map with monsters in the corresponding locations
        for monster in monsters:
            monster_id = monster.id
            self.id_to_monsters[monster_id] = monster
            # Add monster id to a tile
            row, col = monster.getLocation()
            tile = self.map.get_tile(row, col)
            tile.add_monster(monster_id)

    def execute(self, playerAction):
        """
        Executes a player action
        :param playerAction: (string) representing the player action
        :return: a list of game objects that have changed from executing player action
        """
        # TODO: Add player actions to constants.py and implement them here
        pass

    def _get_top_server_map(self):
        """
        Helper method for creating the top portion of the server map
        :return: the top of the server map (grid portion)
        """
        divider = "{}".format('-'*(self.map_constants.DIVIDER_MULTIPLIER*self.map.columns+1))

        # Generate the top half of the map (grid)
        map_list = ["{}<br>".format(divider)] # list to hold to the string representation of the map temporarily
        for row in range(self.map.rows):
            for col in range(self.map.columns):
                map_list.append("|")
                tile_number = str(self.map.coords_to_number(row, col))

                # Add padding to make this tile the same size as the other tiles
                if len(tile_number) < self.map_constants.TILE_SIZE:
                    spaces = '&nbsp&nbsp' *  (self.map_constants.TILE_SIZE - len(tile_number))
                    tile_number = spaces + tile_number

                map_list.append(tile_number)
                # append "|" at the end of a row
                if col == self.map.columns - 1:
                    map_list.append("|")
            map_list.append("<br>{}<br>".format(divider)) # add a divider --------- at the end of each row
        map_list.append("<br>")
        return ''.join(map_list)

    def _get_bottom_server_map(self):
        """
        Helper method for creating the bottom portion of the server map
        :return: the bottom of the server map (objects portion)
        """
        map_list =  []
        # Generate the bottom half of the map (tile_number : game objects at that location)
        for tile_number in range(self.map.get_number_of_tiles()):
            # Get the tile at that location
            row, col = self.map.number_to_coords(tile_number)
            tile = self.map.get_tile(row, col)
            # Add the tile string representation if the tile is not empty
            if not tile.is_empty():
                indent = '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' * self.map_constants.TILE_INDENT
                temp_list = ["[{}]:<br>".format(tile_number)]  # temporary list to hold the string representation of the tile
                # Add all the players to the string
                if tile.players:
                    temp_list.append(indent + "Player(s):<br>")
                    for player_id in tile.players:
                        player = self.id_to_players[player_id]
                        temp_list.append(indent * 2 + "{}<br>".format(player.__str__(self.map_constants.ONLY_ID)))
                # Add all the monsters to the string
                if tile.monsters:
                    temp_list.append(indent + "Monster(s):<br>")
                    for monster_id in tile.monsters:
                        monster = self.id_to_monsters[monster_id]
                        temp_list.append(indent * 2 + "{}<br>".format(monster.__str__(self.map_constants.ONLY_ID)))
                map_list.extend(temp_list)

        # Finally, return the map as a sting
        return ''.join(map_list)[:-1] # remove the last new line

    def get_server_map(self):
        """
        :return: (string) a map of the game from the perspective of the server with all
                    monsters and players visible where the top is a numbered grid of the board and the bottom is
                    a list of all the players and monsters on each of the tiles
        """
        return self._get_top_server_map() + self._get_bottom_server_map()


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
        print(game.get_server_map())