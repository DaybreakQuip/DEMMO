import sys
sys.path.append('__HOME__/DEMMO')

from database import Database, Serialize, Deserialize
from containers.player import Player
from containers.monster import Monster

def handle_get(request):
    """
    # TODO: Add more options to this / refine it
    Handles GET requests
    :param request: the current get request
    :return: result from GET request
    """
    values = request.get('values', {})
    # TODO: Catch exceptions
    option = values['option']
    if option== "map":
        game = Deserialize.createGameFromDatabase()
        return game.get_server_map()
    elif option == "player":
        player_id = values['id']
        player = Database.get_player_info(player_id)
        return str(Deserialize.createPlayerObject(player))

def handle_post(request):
    """
    Handle POST requests
    :param request: request containing 'player_id' and 'action' inside the 'form' of the request
    :return: response based on request
    """
    # Get arguments from the request
    form = request.get('form', {})
    player_id = form['player_id']
    action = form['action']

    changed_game_objects = [] # list of game objects that have changed

    # Create a game from the database
    game = Deserialize.createGameFromDatabase()
    # If the player_id does not exist, create a new player and add it to the game
    if player_id not in game.id_to_players:
        player = Player(player_id)
        game.add_player(player)
        changed_game_objects.append(player)

    # Execute the player's action and keep track of game objects that changed
    changed_game_objects.extend(game.execute(player_id, action))

    # Update and store all game objects that have changed
    Serialize.updateGameObjects(changed_game_objects)
    game = Deserialize.createGameFromDatabase()
    health, power, gold, bosses = game.get_player_stats(player_id)
    return "{}, {}, {}, {},|{}".format(health, power, gold, bosses, game.get_surrounding_entities(player_id))

def request_handler(request=None):
    method = request.get("method")
    if method == "GET":
        return handle_get(request)
    elif method == "POST":
        return handle_post(request)
    else:
        return "Invalid request: {}".format(request)