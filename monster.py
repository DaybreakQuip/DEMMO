from game_object import GameObject

class Monster(GameObject):
    def __init__(self, id, health, power):
        """
        Initializes a new Monster object
        :param id: id of the monster
        :param health: health of the monster, initial health cannot be < 0
        :param power: power of the monster
        """
        # TODO: Complete monster class by adding more fields and adding methods to
        #       interact with a monster
        super().__init__(id, health, power)

    def inflictDamage(self, damage):
        """
        Damages the monster by a certain amount
        :param damage: the amount of damage dealt to the monster, must be > 0
        """
        self.updateHealth(-damage)