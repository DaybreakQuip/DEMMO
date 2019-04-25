class GameObject():
    """
    Class representing a game object, which is a unit in the game with id, health, and power
    """
    def __init__(self, id, health, power):
        """
        Creates a new game object with id, health, and power
        :param id: id of the object
        :param health: initial health of the object, cannot be < 0
        :param power: initial power of the object
        """
        self.id = id
        self.health = health
        self.power = power

    @property
    def isAlive(self):
        """
        Returns whether the game object is alive or not
        """
        return self.health == 0

    def updateHealth(self, delta):
        """
        Updates the game object's health by delta
        """
        self.health = max(0, self.health+delta)

    def updatePower(self, delta):
        """
        Updates the game object's power by delta
        """
        self.power = max(0, self.power+delta)