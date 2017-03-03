"""Independent snake object for use in Game."""

class Snake:
    """
    Feisty snake object.

    Has the following attributes:
    size            (int)       - > 0, describes length of snake
    identifier      (uuid)      - unique identifier describing for each snake
    positions       ([coords])  - array of [x,y] describing snakes body
    health          (int)       - 0..100, describes moves a snake has before
                                    death, unless that snake eats food.
    old_health      (int)       - health of snake on last move
    old_positions   ([[coords]])- array of array of [x,y] describing past
                                    locations the snake was at
    state           (string)    - (unknown | food | attack | flee), describes
                                    past actions of snake
    taunt           (string)    - snake's current taunt
    name            (string)    - name of snake
    """

    def __init__(self, data):
        """
        Initialize the Snake class.

        param1: data - all snake-related data from server

        Raises: ValueError
            if: size not int.
        """
        # comment out for
        # vv SPEED
        self.isString(data['identifier'], 'identifier')
        # ^^ SPEED

        # often updated
        self.identifier = data['id']
        self.positions = data['positions']
        self.health = data['health']
        # old
        self.old_size = len(self.positions)
        self.old_health = data['health']
        self.old_positions = [data['positions']]
        # snake personality
        self.taunt = data['taunt']
        self.name = data['name']

        self.state = 'unknown'

    def update(self, data):
        """
        Update snake after previous move.

        param1: array - [x, y] of current head position of the snake.
        param2: bool - whether the snake ate food in last turn.
        param3: health - snake's most recent health.
        """

        health = data['health']
        if health > 100 or health < 0:
            raise ValueError('health must be between 100 and 0')

        self.old_health = self.health
        self.health = health

        self.positions = data['coords']

        self.old_positions.insert(0, self.positions)

    def getSize(self):
        """
        Return snake size
        return: int - snake
        """

        return len(self.positions)

    def getHealth(self):
        """"
        Return snake health
        return: int - health
        """

        return self.health

    def getHunger(self):
        """
        Return hunger of snake

        return: int - 100-health.
        """

        return 100 - self.health

    def getHeadPosition(self):
        """
        Return head position.
        return: array - as [x, y] coords.
        """

        return self.positions[0]

    def getAllPositions(self):
        """
        Return array of positions.

        return: array[array] - [x,y] of all body coords.
        """

        return self.positions

    def getTailPosition(self):
        """
        Return array of tail position.

        return: array - [x, y] of tail coords
        """

        return self.positions[-1]

    def setState(self, state):
        """
        Set snake state. One of (unknown | food | attack | flee).

            Raises: ValueError
                if: state does not match four options
        """
        if state == 'unknown' or state == 'food' or state == 'attack' or \
        state == 'flee':
            self.state = state
            return
        else:
            raise ValueError('invalid state')

    def getState(self):
        """
        Return snake state.

        return: string
        """

        return self.state

    def getIdentifier(self):
        """
        Return snake's identifier.

        return: uuid (as string)
        """

        return self.identifier

    def toString(self):
        """
        Return Snake attribues as a string.
        """

        asString = "identifer: " + str(self.identifier) + "\n\
health: " + str(self.health) + "\n\
size: " + str(len(self.positions)) + "\n\
state: " + str(self.state) + "\n\
positions: " + str(self.positions)

        return asString

    @staticmethod
    def isInt(num, name):
        """Double check value is int."""
        if not isinstance(num, int):
            raise ValueError(str(name) + ' must be an integer')

    @staticmethod
    def isString(value, name):
        """Double check value is int."""
        if not isinstance(value, str):
            raise ValueError(str(name) + ' must be a string')
