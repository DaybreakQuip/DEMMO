import sys
sys.path.append('__HOME__/DEMMO')

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
        width = self.columns  # number of columns = width of the map
        return row * width + col

    def get_number_of_tiles(self):
        return self.rows * self.columns

    def get_tile(self, row, col):
        return self.tiles[row][col]

    def is_coordinate_in_range(self, row, col):
        return 0 <= row <= self.rows - 1 and 0 <= col <= self.columns - 1

    def __str__(self):
        string = ""
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                tile = self.tiles[row][col]
                string += "({}, {})\n".format(row, col)
                string += tile.__str__() + '\n'
        return string[:-1]

class Tile:
    """
    Class representing a single tile, which can be populated by players and/or monsters
    """

    def __init__(self):
        """
        Creates a new tile that contains a list of players and monsters i
        """
        self.players = set()  # set of player ids
        self.monsters = set()  # set of monster ids

    def has_player(self, player_id):
        return player_id in self.players

    def has_monster(self):
        return len(self.monsters) > 0

    def get_monster(self):
        # Return the only monster in the monsters set
        # TODO: quite janky, change tile in the future to hold only one monster
        for monster in self.monsters:
            return monster

    def add_player(self, player_id):
        self.players.add(player_id)

    def remove_player(self, player_id):
        self.players.remove(player_id)

    def add_monster(self, monster_id):
        self.monsters.add(monster_id)

    def remove_monster(self, monster_id):
        self.monsters.remove(monster_id)

    def get_number_of_players(self):
        return len(self.players)

    def get_number_of_monsters(self):
        return len(self.monsters)

    def is_empty(self):
        return not (self.players or self.monsters)

    def __str__(self, base_indent=0, only_id=False):
        """
        Returns a string representation of a Tile object
        :param base_indent: (int) base indent level for the string
        :param only_id: (bool) indicating whether only the id of the game object will be shown
        :return: (string) string rep of the tile
        """
        indent = '\t' * base_indent
        temp_list = []  # temporary list to hold the string representation of the tile
        # Add all the players to the string
        if self.players:
            temp_list.append(indent + "Player(s):\n")
            for player in self.players:
                temp_list.append(indent + "\t{}\n".format(player))
        # Add all the monsters to the string
        if self.monsters:
            temp_list.append(indent + "Monster:\n")
            for monster in self.monsters:
                temp_list.append(indent + "\t{}\n".format(monster))
        return ''.join(temp_list)