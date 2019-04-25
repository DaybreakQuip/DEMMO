import sys
sys.path.append('__HOME__/DEMMO')

from database import Database, Serialize, Deserialize
from containers.player import Player
from containers.monster import Monster

def handle_get(request):
    """
    # TODO: Add more options to this / refine it
    Handles GET request
    :param request: the current get request
    :return: result from GET request
    """
    values = request.get('values', {})
    # TODO: Catch exceptions
    option = values['option']
    if option== "game_map":
        game = Deserialize.createGameFromDatabase()
        return game.get_server_map()
    elif option == "player":
        player_id = values['id']
        player = Database.get_player_info(player_id)
        return str(Deserialize.createPlayerObject(player))

def handle_post(request):
    form = request.get('form', {})

    # TODO: Change this to player_id & action in the future, for now it is just creating
    #       a player with that id in that location (row, col)

    # TODO: Catch exceptions
    player_id = form['player_id']
    row = int(form['row'])
    col = int(form['col'])
    # Create a new player
    player = Player(id, row, col)
    # Add player to database
    Serialize.updatePlayer(player)
    # Return information about the player just added
    return player

def request_handler(request=None):
    method = request.get("method")
    if method == "GET":
        return handle_get(request)
    elif method == "POST":
        return handle_post(request)
    else:
        return "Invalid request: {}".format(request)