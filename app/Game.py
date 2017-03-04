"""Process all game data. Handles getting in new board states, analyzing snake
health, and providing Main with the best next move."""

import sys
from Snake import Snake
from Board import Board


class Game:
    """Allow for several Battlesnake games to be played at once by providing
    several different Game objects.

    Has following attributes:
    weightGrid      (board)     - Board object
    width           (int)       - Board width
    height          (int)       - Board height
    you             (string)    - UUID representing what our snake's ID is
    food   (array)     - array of coord arrays
    turn            (int)       - 0-indexed int representing completed turns
    snakes          (dict)      - dict of Snake objects currently in play
    deadSnakes      (dict)      - dict of Snake objects that no longer compete"""

    def __init__(self, data):
        """Initialize the Game class.

        param1: dictionary - all data from /start POST.
        """
        self.weightGrid = Board(data['width'], data['height'])
        self.width = data['width']
        self.height = data['height']

        self.snakes = {}
        self.you = ''
        self.food = []
        self.turn = 0
        self.deadSnakes = []

    def update(self, data):
        """Update game with current board from server.

        param1: dictionary - all data from response. See Battlesnake docs
        for more info."""
        for snakeData in data['snakes']:
            if snakeData['id'] in self.snakes:
                self.snakes[snakeData['id']].update(snakeData)
            else:
                self.snakes[snakeData['id']] = Snake(snakeData)

        self.food = data['food']
        self.you = data['you']
        if 'dead_snakes' in data:
            self.deadSnakes = data['dead_snakes']
            for snake in self.deadSnakes:
                if snake['id'] in self.snakes:
                    del self.snakes[snake['id']]


    def getNextMove(self):
        """"Use all algorithms to determine the next best move for our snake."""

        # RUN WEIGHTING ALGORITHMS HERE

        self.weightNotHitSnakes()

        # RUN WEIGHTING ALGORITHMS HERE

        topPriorityNode = self.weightGrid.getNodeWithPriority(0)
        if self.weightGrid.isNodeWeightUnique(topPriorityNode):
            return self.convertNodeToDirection(topPriorityNode, self.you)


        numDuplicates = self.weightGrid.countNodeWeightCopies(topPriorityNode)

        duplicateNodes = self.weightGrid.getNodesWithPriority(0, numDuplicates - 1)
        closestLen = sys.maxint
        closestPos = []
        for node in duplicateNodes:
            tempLen = self.weightGrid.optimumPath(self.snakes[self.you].getHeadPosition(), node)
            print tempLen
            if tempLen < closestLen:
                closestLen = tempLen
                closestPos = node
            print node
        print closestPos
        return self.convertNodeToDirection(closestPos, self.you)


    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and it self"""
        us = self.snakes[self.you] #Represents our snakes
        ourSnakePos = us.getAllPositions()
        ourTail = ourSnakePos[-1] #[[x, y],[x,y]]=
        ourTailX = ourTail[0]
        ourTailY = ourTail[1]

        for s in self.snakes:
            positions = self.snakes[s].getAllPositions()
            self.weightGrid.setWeights(positions, 0)
            """for x in positions:
                for y in positions[x]:
                    pos = x+','+y
                    self.weightGrid.setWeight(pos, 0)"""
        #TODO
        #Weight self as 0
        #Are we getting food this move? (Do we need to weight our tail 0)
            #Check if head position is in old food positions.
        #Weight other snakes as 0
        #Are they getting food this move? (Do we need to weigh their tails 0)
        #Are they dying this move?
        #How big are they? Don't block heads of small snakes


    def weightFood(self):
        """Weight grid with food necessity"""
        #TODO
            #How desperately do we need food
            #Goes through all food and returns the closest according to optimumPath
        foodCoord = 0
        pathLength = 500
        shortestPath = sys.maxint
        closestFoodCoord = 0
        oursnake = self.snakes[self.you]
        head = oursnake.getHeadPosition()
        health = oursnake.getHealth()
        for foodCoords in self.food:
            pathLength = len(self.weightGrid.optimumPath(head, foodCoords))
            if pathLength < shortestPath:
                shortestPath = pathLength
                closestFoodCoord = foodCoord

            foodCoord += 1
            foodWeight = 100 - health - pathLength # this will change based on
                                                   # health decrementation
            self.weightGrid.setWeight(foodCoords, foodWeight)
        if health > 30:
            return False

        return self.weightGrid.optimumPath(head, self.food[closestFoodCoord])


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


    def convertNodeToDirection(self, node, identifer):
        """
        Convert a coord array into an up, down, left, right direction.
        param1: [int,int] - x,y coords of a node.
        param2: string - id of some snake in the game (ie, in snakes{})

        Raises: ValueError
            if: node is not adjacent to the snakes head

        return: string - direction to go
        """

        snake = self.snakes[identifer]
        head = snake.getHeadPosition()

        if node[0] == (head[0] + 1):
            return 'right'
        if node[0] == (head[0] - 1):
            return 'left'
        if node[1] == (head[1] + 1):
            return 'up'
        if node[1] == (head[1] - 1):
            return 'down'
        else:
            raise ValueError('node must be adjacent')

# Example code testing
if __name__ == '__main__':
    INITDATA = {"width": 20, "height": 20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"}
    b = Game(INITDATA)
    b.weightGrid.showWeights(True, True)
    print b.getNextMove()
