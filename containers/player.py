import sys
sys.path.append('__HOME__/DEMMO')

from containers.game_object import GameObject
import constants

class Player(GameObject):
    def __init__(self, id, row, col, health=constants.Player.DEFAULT_HEALTH,
                                     power=constants.Player.DEFAULT_POWER,
                                     gold=constants.Player.DEFAULT_GOLD,
                                     num_boss_defeated=constants.Player.DEFAULT_BOSS_DEFEATED):
        """
        Initializes a new Player object
        :param id: player id
        :param row: (int) row of the object
        :param col: (int) col of the object
        :param health: health of the player, initial value cannot be < 0
        :param power: power of the player
        :param gold: gold of the player
        """
        # TODO: Complete player class by adding more fields and adding methods to
        #       interact with a player
        super().__init__(id, row, col, health, power)
        self.gold = gold
        self.num_boss_defeated = num_boss_defeated

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

    def move_up(self):
        """
        Move the character up one spot
        :return:
        """
        # TODO Implement me
        pass

    def move_south(self):
        """
        Move the player down one spot
        :return:
        """
        # TODO: Implement me
        pass

    def move_left(self):
        """
        Move the player left one spot
        :return:
        """
        # TODO: Implement me
        pass

    def move_right(self):
        """
        Move the player right one spot
        :return:
        """
        # TODO: implement me
        pass

    def __str__(self, only_id=False):
        """
        :return: string representation of the game object
        """
        if only_id:
            return self.id

        return "(id: {}, health: {}, power: {}, gold: {}, bosses defeated: {})".format(
            self.id, self.health, self.power, self.gold, self.num_boss_defeated
        )


if __name__ == '__main__':
    if constants.TESTING:
        player = Player("Bob", 0, 0)
        print(player)