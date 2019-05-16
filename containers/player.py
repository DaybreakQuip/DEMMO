import sys
sys.path.append('__HOME__/DEMMO')

from containers.game_object import GameObject
import constants

class Player(GameObject):
    def __init__(self, id, row=constants.Player.DEFAULT_ROW,
                           col=constants.Player.DEFAULT_COL,
                           health=constants.Player.DEFAULT_HEALTH,
                           power=constants.Player.DEFAULT_POWER,
                           luck = constants.Player.DEFAULT_LUCK,
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
        self.luck = luck
        self.gold = gold
        self.num_boss_defeated = num_boss_defeated

    def buy_health(self):
        """
        Increases player health by 5 if the player has enough gold to purchase more health
        :return: true if the purchase was successful and false otherwise
        """
        cost = int(pow(self.health, constants.Game.SHOP_EXPONENT))
        if self.gold >= cost:
            self.gold -= cost
            self.health += constants.Game.HEALTH_INCREASE
            return True
        return False

    def buy_power(self):
        """
        Increases player power by 1 if the player has enough gold to purchase more health
        :return: true if the purchase was successful and false otherwise
        """
        cost = int(pow(self.power, constants.Game.SHOP_EXPONENT))
        if self.gold >= cost:
            self.gold -= cost
            self.power += constants.Game.POWER_INCREASE
            return True
        return False

    def buy_luck(self):
        """
        Increases player luck by 1 if the player has enough gold to purchase more luck
        :return: true if the purchase was successful and false otherwise
        """
        cost = int(pow(self.luck, constants.Game.SHOP_EXPONENT))
        if self.gold >= cost:
            self.gold -= cost
            self.luck += constants.Game.LUCK_INCREASE
            return True
        return False

    def move_up(self):
        """
        Move the character up one spot
        :return:
        """
        # TODO Implement me
        if 0 < self.row <= 9:
           self.row -= 1
        return self

    def move_down(self):
        """
        Move the player down one spot
        :return:
        """
        if 0 <= self.row < 9:
            self.row += 1
        return self
    def move_left(self):
        """
        Move the player left one spot
        :return:
        """
        if 0 < self.col <= 9:
            self.col -= 1
        return self
    def move_right(self):
        """
        Move the player right one spot
        :return:
        """
        if 0 <= self.col < 9:
            self.col += 1
        return self

    def get_gold(self):
        return self.gold

    def get_luck(self):
        return self.luck

    def get_number_of_bosses_defeated(self):
        return self.num_boss_defeated

    def get_player_stats(self):
        """
        :return: player stats
        """
        return self.get_health(), self.get_power(), self.get_luck(), self.get_gold(), self.get_number_of_bosses_defeated()

    def __str__(self, only_id=False):
        """
        :return: string representation of the game object
        """
        if only_id:
            return self.id

        return "(id: {}, health: {}, power: {}, luck: {}, gold: {}, bosses defeated: {})".format(
            self.id, self.health, self.power, self.luck, self.gold, self.num_boss_defeated
        )


if __name__ == '__main__':
    if constants.TESTING:
        player = Player("Bob", 0, 0)
        print(player)