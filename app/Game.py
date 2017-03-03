"""Process all game data. Handles getting in new board states, analyzing snake
health, and providing Main with the best next move."""
from Snake import Snake
from Board import Board



class Game:
    """Allow for several Battlesnake games to be played at once by providing
    several different Game objects."""

    def __init__(self, data):
        """Initialize the Game class"""
        #TODO
        #Init weight grid, init grid graph ** not 100% sure about relationship here, maybe graph should have grid as a child to make pathing decisions **
        self.weightGrid = Board(data['width'],data['height'])
        self.snakes = {}
        self.you = data['you']
        self.foodPositions = data['food']
        self.width = data['width']
        self.height = data['height']
        self.turn = data['turn']
        
        #Init snakes

    def update(self, snakesData, foodPositions):
        """Update game with current board from server"""
        #TODO
            #Calculate all game changes and store

        #Creates a list of snakes in the game
        snakeArr = []
        for x in snakesData:
            identity = snakesData[x]['id']
            hp = snakesData[x]['health_points']
            coords = snakesData[x]['health_points']
            size = len(coords)

            snakeArr.append(Snake(size, coords, hp, identity))


    def getNextMove(self):
        """"Use all algorithms to determine the next best move for our snake"""
        #TODO
            #Run each algorithm to make decisions
            #Find best route to desired square
            #Ensure boundary is not selected (shouldn't be an issue since we would only head towards positively weighted squares anyway and boundary square do not exist according to algorithm)
            #If several candidates, pick one at random
            #Return decision


    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and it self"""
        us = 0
        for s in self.snakes:
            if(s.identifier == self.you):
                us = s

        for s in self.snakes:
            positions = s.getAllPositions()
            for x in positions:
                for y in positions[x]:
                    pos = x+','+y
                    self.weightGrid.setWeight(pos,0)
        #TODO
        #Weight self as 0
        #Are we getting food this move? (Do we need to weight our tail 0)
        #Weight other snakes as 0
        #Are they getting food this move? (Do we need to weigh their tails 0)
        #Are they dying this move?
        #How big are they? Don't block heads of small snakes

    def weightFood(self):
        """Weight grid with food necessity"""
        #TODO
            #How desperately do we need food?
            #How long do we have to get there?


    def weightSmallSnakes(self):
        """Positively weight smaller snakes for murdering purposes"""
        #TODO
            #Compare size
            #How long will it take to get to the snake?
            #How much food is around for the snake to grow?


    def weightLargeSnakes(self):
        """Negativly weight squares where large snake heads could move to next round"""
        #TODO
            #Compare size
            #Can we get food and grow bigger?


    def weightEnclosedSpaces(self):
        """Do not kill ourselves by picking a corner where we trap ourselves"""
        #TODO
            #How long are we?
            #Are we giving other people the opportunity to block off our exit?
            #What is the optimal traversal path to maximize future space opportunities
            #Don't limit our moves (against a surface) unless advantageous or necessary


    def weightTrapSnakes(self):
        """Positively weight squares that will allow us to block other snakes off"""
        #TODO
            #How long are they?
            #How much traversal room are we leaving them?
            #Do they need food? Do they have it in the trapped location?
            #How long are we? Can we effectively block them for long enough?
