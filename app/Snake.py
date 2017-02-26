"""Independent snake object for use in Game."""
class Snake:
    """Feisty snake object."""
    def __init__(self, size, positions, health):
        """Initialize the Snake class"""
        #TODO
            # Init size
            # Init positions queue (can easily pop front when moving forwards and add to back)
            # Init health
            # Init state (unknown, food, attack, flee) - can predict
			#  for other snakes and set based on know values for our own
            # Init list of past positions


    def update(self, headPosition, foodBoolean):
        """Update snake after previous move"""
        #TODO
            # Update positions queue
            # Did we get food? Increase health if yes, decrease health if no
            # Append to past positions


    def getSize(self):
        """Return snake size"""
        #TODO
            # Return size


    def getHealth(self):
        """"Return snake health"""
        #TODO
            # Return health

    def getFoodUrgency(self):
        """How badly do we need food?"""
        
    def getHeadPosition(self):
        """Return head position"""
        #TODO
            # Return head position


    def getAllPositions(self):
        """Return array of positions"""
        #TODO
            # Return array of positions


    def setState(self, state):
        """Set snake state"""
        #TODO
            # Set state


    def getState(self):
        """Return snake state"""
        #TODO
            # Return state
