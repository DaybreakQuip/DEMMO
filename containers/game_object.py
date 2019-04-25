class GameObject():
    """
    Class representing a game object, which is a unit in the game with id, health, and power
    """
    def __init__(self, id, row, col, health, power):
        """
        Creates a new game object with id, health, and power
        :param id: (string) id of the object
        :param row: (int) row of the object
        :param col: (int) col of the object
        :param health: (int) initial health of the object, cannot be < 0
        :param power: (int) initial power of the object
        """
        self.id = id
        self.row = row
        self.col = col
        self.health = health
        self.power = power

    @property
    def isAlive(self):
        """
        Returns whether the game object is alive or not
        """
        return self.health == 0

    def getLocation(self):
        """
        :return: position of the game object with format (row, col)
        """
        return (self.row, self.col)

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

    def __str__(self, only_id=False):
        """
        :return: string representation of the game object
        """
        if only_id:
            return self.id

        return "(id: {}, health: {}, power: {})".format(
            self.id, self.health, self.power
        )