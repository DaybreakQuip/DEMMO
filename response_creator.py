import sys
sys.path.append('__HOME__/DEMMO')

class ResponseCreator:
    """
    Class creating responses for POST requests
    """
    def __init__(self, game):
        """
        Create a new GameResponse
        :param game: the game to create responses from
        """
        self.game = game

    def get_player_info_for_response(self, player_id):
        """
        Returns player stats for a response
        :param player_id: id of the player
        :return: player stats with format: "{}, {}, {}, {}, {},".format(health, power, luck, gold, bosses)
        """
        health, power, luck, gold, bosses = self.game.get_player_stats(player_id)
        return "{}, {}, {}, {}, {},".format(health, power, luck, gold, bosses)

    def get_monster_info_for_response(self, player_id):
        """
        Returns monster stats for a response based on a given player
        :param player_id: player_id of the player
        :return: monster stats with format: ('T'|'F'),{health},{power},{is_boss} of the monster that is located in
        the same spot as a player
        """
        monster = self.game.get_monster_on_top_of_player(player_id)
        if not monster: # if there is no monster on top of the player
            response = "F"
        else:
            health, power, _, _ = monster.get_monster_stats()
            response = "T,{},{}".format(health, power)
        return response

    def get_action_response(self, player_id):
        """
        Returns the response for an action done by the player
        :param player_id: the player's id
        :return: string with format player_info|map_info|monster_info
        """
        player_info = self.get_player_info_for_response(player_id)
        map_info = self.get_surrounding_entities(player_id)
        monster_info = self.get_monster_info_for_response(player_id)

        return "{}|{}|{}".format(player_info, map_info, monster_info)

    def get_surrounding_entities(self, player_id):
        """
        Gets the surrounding entities of the player, if any
        :param player_id: player to locate
        :return: a 3x3 String display of tiles around the player (including the tile the player is on)
        """
        player = self.game.id_to_players[player_id]
        player_row_coord, player_col_coord = player.get_location()
        entities = ""
        for row in range(-1,2):
            for col in range(-1,2):
                neighbor_row = player_row_coord + row
                neighbor_col = player_col_coord + col
                if self.game.map.is_coordinate_in_range(neighbor_row, neighbor_col):
                    tile = self.game.map.get_tile(neighbor_row,neighbor_col)
                    if tile.get_number_of_players() > 0 and tile.get_number_of_monsters() > 0:
                        entities += "MP,"
                    elif tile.get_number_of_monsters() > 0:
                        entities += "M_,"
                    elif tile.get_number_of_players() > 0:
                        entities += "_P,"
                    else:
                        entities += "__,"
                else:
                    entities += "XX,"
        return entities

    def _get_top_server_map(self):
        """
        Helper method for creating the top portion of the server map
        :return: the top of the server map (grid portion)
        """
        divider = "{}".format('-'*(self.game.map_constants.DIVIDER_MULTIPLIER*self.game.map.columns+1))

        # Generate the top half of the map (grid)
        map_list = ["{}\n".format(divider)] # list to hold to the string representation of the map temporarily
        for row in range(self.game.map.rows):
            for col in range(self.game.map.columns):
                map_list.append("|")
                tile_number = str(self.game.map.coords_to_number(row, col))

                # Add padding to make this tile the same size as the other tiles
                if len(tile_number) < self.game.map_constants.TILE_SIZE:
                    spaces = ' ' *  (self.game.map_constants.TILE_SIZE - len(tile_number))
                    tile_number = spaces + tile_number

                map_list.append(tile_number)
                # append "|" at the end of a row
                if col == self.game.map.columns - 1:
                    map_list.append("|")
            map_list.append("\n{}\n".format(divider)) # add a divider --------- at the end of each row
        map_list.append("\n")
        return ''.join(map_list)

    def _get_bottom_server_map(self):
        """
        Helper method for creating the bottom portion of the server map
        :return: the bottom of the server map (objects portion)
        """
        map_list =  []
        # Generate the bottom half of the map (tile_number : game objects at that location)
        for tile_number in range(self.game.map.get_number_of_tiles()):
            # Get the tile at that location
            row, col = self.game.map.number_to_coords(tile_number)
            tile = self.game.map.get_tile(row, col)
            # Add the tile string representation if the tile is not empty
            if not tile.is_empty():
                indent = '\t' * self.game.map_constants.TILE_INDENT
                temp_list = ["[{}]:\n".format(tile_number)]  # temporary list to hold the string representation of the tile
                # Add all the players to the string
                if tile.players:
                    temp_list.append(indent + "Player(s):\n")
                    for player_id in tile.players:
                        player = self.game.id_to_players[player_id]
                        temp_list.append(indent * 2 + "{}\n".format(player.__str__(self.game.map_constants.ONLY_ID)))
                # Add all the monsters to the string
                if tile.monsters:
                    temp_list.append(indent + "Monster(s):\n")
                    for monster_id in tile.monsters:
                        monster = self.game.id_to_monsters[monster_id]
                        temp_list.append(indent * 2 + "{}\n".format(monster.__str__(self.game.map_constants.ONLY_ID)))
                map_list.extend(temp_list)

        # Finally, return the map as a sting
        return ''.join(map_list)[:-1] # remove the last new line

    def get_server_map(self):
        """
        :return: (string) a map of the game from the perspective of the server with all
                    monsters and players visible where the top is a numbered grid of the board and the bottom is
                    a list of all the players and monsters on each of the tiles
        """
        return "<xmp>" + self._get_top_server_map() + self._get_bottom_server_map() + "</xmp>"