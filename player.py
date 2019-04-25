from game_object import GameObject

class Player(GameObject):
    def __init__(self, id, health, power, gold):
        """
        Initializes a new Player object
        :param id: player id
        :param health: health of the player, initial value cannot be < 0
        :param power: power of the player
        :param gold: gold of the player
        """
        # TODO: Complete player class by adding more fields and adding methods to
        #       interact with a player
        super().__init__(id, health, power)
        self.gold = gold

    def buy_health(self):
        """
        Increases player health by 1 if the player has enough gold to purchase more health
        :return: true if the purchase was successful and false otherwise
        """
        # TODO: Increase player health by 1 if the player has enough gold to purchase the health
        pass

    def buy_power(self):
        """
        Increases player power by 1 if the player has enough gold to purchase more health
        :return: true if hte purchase was successful and false otherwise
        """
        # TODO: Increase player power by 1 if hte player has enough gold to purchase the health
        pass