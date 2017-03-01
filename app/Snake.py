"""Independent snake object for use in Game."""
class Snake:
    """Feisty snake object.

    Has the following states:
        size (int): > 0, describes length of snake
        identifier (uuid): unique identifier describing for each snake
        positions (array[array): array of [x,y] describing snakes body
        health (int): 0..100, describes moves a snake has before death, unless
            that snake eats food.
        old_positions (array[array[array]]): array of array of [x,y] describing
            past locations the snake was at @dfrankcom ?
        state (string): (unknown | food | attack | flee), describes past actions
            of snake
    """
    def __init__(self, size, positions, health, identifier):
        """Initialize the Snake class.

        param1: int - length of snake
        param2: array[array] - each element is a coord value
                                from 0..width, 0..height and describes one body
                                cell of a snake
        param3: int - health of snake
        param4: uuid - assigned ID for each snake

        Raises: ValueError
            if: size not int.
        """

        if not isinstance(size, int):
            raise ValueError('size must be an integer')
        if size <= 1:
            raise ValueError('size must be greater than 1')
        self.size = size
        self.identifier = identifier
        self.positions = positions
        self.health = health
        self.old_positions = [positions]

        self.state = 'unknown' # will be updated later
        #TODO
            # Init list of past positions
                # @dfrankcom - is Line 27 what you meant?


    def update(self, headPosition, foodBoolean, health):
        """Update snake after previous move.

        param1: array - [x, y] of current head position of the snake.
        param2: 'true' or 'false' - whether the snake ate food in last turn.
        param3: health - snake's most recent health"""
        if  not isinstance(health, int):
            raise ValueError('health must be an integer')
        if health > 100 or health < 0:
            raise ValueError('health must be between 100 and 0')

        self.health = health

        self.positions.insert(0, headPosition)
        if foodBoolean != 'true':
            del self.positions[-1]

        self.old_positions.insert(0, self.positions)

    def getSize(self):
        """Return snake size
        return: int"""

        return self.size

    def getHealth(self):
        """"Return snake health
        return: int"""

        return self.health

    def getFoodUrgency(self):
        """How badly do we need food?

        return: float 0..1 scale of how much this snake needs food"""

        #TODO
            # Choose way to represent food urgency (0..1? 0..100?)
            # Create equation

    def getHeadPosition(self):
        """Return head position.
        return: array - as [x, y] coords."""

        return self.positions[0]

    def getAllPositions(self):
        """Return array of positions.

        return: array[array] - [x,y] of all body coords."""

        return self.positions

    def setState(self, state):
        """Set snake state. One of (unknown | food | attack | flee).

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
        """Return snake state.

        return: string"""

        return self.state

    def toString(self):
        """Return Snake attribues as a string."""

        asString = "identifer: " + str(self.identifier) + "\n\
health: " + str(self.health) + "\n\
size: " + str(self.size) + "\n\
state: " + str(self.state) + "\n\
positions: " + str(self.positions)

        return asString
