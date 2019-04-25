class Game:
    """
    Class representing an on-going DEMMO game
    """
    def __init__(self, height, width, players, monsters):
        """
        Initializes a new game object with players, monster, and a map of the game
        :param height: height of the game map
        :param width: width of the game map
        :param players: list of players in the game
        :param monsters: list of monsters in the game
        """
        self.height = height
        self.width = width
        self.players = players
        self.monsters = monsters

    def execute(self, playerAction):
        """
        Executes a player action
        :param playerAction: a string representing the player action
        :return: true if the action succeeded and false otherwise
        """
        # TODO: Add player actions to constants.py and implement them here
        pass