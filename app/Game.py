"""Process all game data. Handles getting in new board states, analyzing snake
health, and providing Main with the best next move."""

import sys
import random
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
        self.deadSnakes = {}
        self.newDead = 'False'      #Stores new deaths as id so must be string

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
        if 'turn' in data:
            self.turn = data['turn']

        #Checks if there are any new dead snakes, and removes them from snakes{}
        self.newDead = False
        if 'dead_snakes' in data:
            for deadSnake in data['dead_snakes']:
                snakeId = deadSnake['id']
                if snakeId in self.snakes and snakeId not in self.deadSnakes:
                    del self.snakes[deadSnake['id']]
                    self.deadSnakes[deadSnake['id']] = deadSnake
                    self.newDead = deadSnake['id']

    def showBoard(self):
        """Use to show board with weight and colours """
        print "Running showBoard"
        self.weightGrid.showWeights(True, True)


    def getNextMove(self):
        """"Use all algorithms to determine the next best move for our snake."""

        self.weightGrid.resetWeights()

        # RUN WEIGHTING ALGORITHMS HERE

        self.weightNotHitSnakes()
        self.weightFood()
        self.weightSmallSnakes()
        self.weightLargeSnakes()

        # RUN WEIGHTING ALGORITHMS HERE

        self.weightGrid.setEdges()
        # self.weightGrid.averageWeights(5)

        target = []
        usSnake = self.snakes[self.you]

        priorityTarget = 0
        nodeValid = False

        while not nodeValid:
            topPriorityNode = self.weightGrid.getNodeWithPriority(priorityTarget)
            if self.weightGrid.isNodeWeightUnique(topPriorityNode):
                target = topPriorityNode
                priorityTarget += 1
            else:
                numDuplicates = self.weightGrid.countNodeWeightCopies(topPriorityNode)
                duplicateNodes = self.weightGrid.getNodesWithPriority(priorityTarget, \
                priorityTarget + numDuplicates - 1)
                closestLen = sys.maxint
                closestPos = []

                for node in duplicateNodes:
                    tempPath = self.weightGrid.optimumPath(usSnake.getHeadPosition(), node)
                    tempLen = len(tempPath)

                    if tempLen < closestLen and self.weightGrid.optimumPathLength(\
                    usSnake.getHeadPosition(), node) != float('inf'):
                        closestLen = tempLen
                        closestPos = node

                priorityTarget += numDuplicates

                target = closestPos

            if target == []:
                nodeValid = False
            elif self.weightGrid.optimumPathLength(usSnake.getHeadPosition(), target) != \
            float('inf'):
                nodeValid = True

        #self.weightGrid.showWeights(True, True)


        nextMove = self.weightEnclosedSpaces(target)
        print "Following path: " + str(self.weightGrid.optimumPath(usSnake.getHeadPosition(),\
        nextMove))
        return self.convertNodeToDirection(nextMove, self.you)

    def getTaunt(self):
        """Return taunt for the move request."""

        taunts = ['Do you have any non-GMO food?', 'War. War never changes', 'Sssssslithering',\
         'Snakes? I hate snakes', 'Where can a snake get a bite to eat around here', 'up', 'down',\
          'left', 'right', 'Trying to catch garter snakes']

        nextTaunt = random.choice(taunts)

        #If a snake died last turn, taunt them and clear the newDead variable
        if self.newDead != False:
            deadSnake = self.deadSnakes[self.newDead]
            nextTaunt = 'RIP ' + deadSnake['name'] + ', turn 0 -> turn ' + str(self.turn - 1)
            self.newDead = False

        return nextTaunt


    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and itself."""
        # pylint: disable=E1121

        for s in self.snakes:
            print s
            positions = self.snakes[s].getAllPositions()
            head = positions[0]
            tail = positions[-1]
            self.weightGrid.setWeights(positions, 0.0)
            self.weightGrid.setWeight(tail, 50.0)

            # if snake could eat food, avoid the tail
            # above by 1
            if (head[1]) > 0 and [head[0], head[1] - 1] in self.food:
                self.weightGrid.setWeight(tail, 0.0)
            # left by 1
            if (head[0]) <= self.width and [head[0] + 1, head[1]] in self.food:
                self.weightGrid.setWeight(tail, 0.0)
            # right by 1
            if (head[0]) > 0 and [head[0] - 1, head[1]] in self.food:
                self.weightGrid.setWeight(tail, 0.0)
            # below
            if (head[1]) <= self.height and [head[0], head[1] + 1] in self.food:
                self.weightGrid.setWeight(tail, 0.0)


    def weightFood(self):
        """Weight grid with food necessity"""
        #TODO
            #How desperately do we need food
            #Goes through all food and returns the closest according to optimumPath
        pathLength = 500
        shortestPath = sys.maxint
        oursnake = self.snakes[self.you]
        head = oursnake.getHeadPosition()
        health = oursnake.getHealth()
        for foodCoords in self.food:
            pathLength = len(self.weightGrid.optimumPath(head, foodCoords))
            if pathLength < shortestPath:
                shortestPath = pathLength
                #closestFoodCoord = foodCoords


            #foodCoord += 1
            foodWeight = 100# - health - pathLength # this will change based on

                                                   # health decrementation
            self.weightGrid.setWeight(foodCoords, foodWeight)



    def weightSmallSnakes(self):
        """Positively weight smaller snakes for murdering purposes"""
        #TODO
            #Compare size
            #How long will it take to get to the snake?
            #How much food is around for the snake to grow?
        oursnake = self.snakes[self.you]
        ourSize = oursnake.getSize()
        weightAdd = 0

        for otherSnake in self.snakes:
            if otherSnake != self.you:
                otherSnakeSize = self.snakes[otherSnake].getSize()
                if  otherSnakeSize < ourSize:
                    """Run this code for every snake on the board that's
                    not you AND smaller than you"""
                    headA = self.headArea(self.snakes[otherSnake])
                    #this algorithm could be altered to add varying values not just a blanket range
                    weightAdd = 12
                    for headCoord in headA:
                        self.weightGrid.addWeight(headCoord, weightAdd)


    def headArea(self, snek):
        """Return an area around the head so that it can be weighted
        param1: snake whose head area needs to be evaluated"""

        #TODO
            #find head
            #find area
            #find body
            #return coordinates
        head = snek.getHeadPosition()
        xCoord = head[0]
        yCoord = head[1]
        upperBoundX = xCoord+2
        upperBoundY = yCoord+2
        lowerBoundX = xCoord-2
        lowerBoundY = yCoord-2
        newCoordinates = []
        if upperBoundY >= self.height:
            upperBoundY = self.height-1
        if upperBoundX >= self.width:
            upperBoundX = self.width-1
        if lowerBoundY < 0:
            lowerBoundY = 0
        if lowerBoundX < 0:
            lowerBoundX = 0
        #goes through a 5x5 grid around the snake and creates an array of those coordinates
        for xCoordNew in range(lowerBoundX, upperBoundX+1):
            for yCoordNew in range(lowerBoundY, upperBoundY+1):
                newCoordinates.append([xCoordNew, yCoordNew])
        #removes any body segments from the grid
        for otherSnakes in self.snakes:
            for bodySegment in self.snakes[otherSnakes].getAllPositions():
                #Run this code for all body (and head) segments of all snakes
                if bodySegment in newCoordinates:
                    newCoordinates.remove(bodySegment)
        #return new bodyless coordinates
        return newCoordinates




    def weightLargeSnakes(self):
        """Negativly weight squares where larger snake heads could move to next round"""

        ourSnake = self.snakes[self.you]
        ourSize = ourSnake.getSize()
        for otherSnake in self.snakes:
            if otherSnake != self.you:
                otherSnakeSize = self.snakes[otherSnake].getSize()
                if  otherSnakeSize >= ourSize:
                    """Run this code for every snake on the board that's
                    not you AND longer or equal to you"""
                    headCoords = self.snakes[otherSnake].getHeadPosition()
                    x = headCoords[0]
                    y = headCoords[1]
                    """Weight coordinates left and right to 0, provided that
                    they are within the board indices (0 - width-1)"""
                    if x > 0:
                        if x < self.width-1:
                            self.weightGrid.setWeights([[x+1, y], [x-1, y]], 0)
                        else:
                            self.weightGrid.setWeights([[x-1, y]], 0)
                    else:
                        self.weightGrid.setWeights([[x+1, y]], 0)

                    """Weight coordinates up and down to 0, provided that
                    they are within the board indices (0 - height-1)"""
                    if y > 0:
                        if y < self.height-1:
                            self.weightGrid.setWeights([[x, y+1], [x, y-1]], 0)
                        else:
                            self.weightGrid.setWeights([[x, y-1]], 0)
                    else:
                        self.weightGrid.setWeights([[x, y+1]], 0)

    def weightEnclosedSpaces(self, u):
        """Negatively weight enclosed spaces to prevent us from going in."""

        # print self.snakes[self.you].getAllPositions()[-1]
        # print u
        #self.weightGrid.showWeights(True, True)
        tailPos = self.snakes[self.you].getTailPosition()
        h = self.snakes[self.you].getAllPositions()[0]
        path = self.weightGrid.optimumPath(h, u) #Current goal
        self.weightGrid.setWeight(tailPos, 1)
        self.weightGrid.setEdges()
        if self.weightGrid.optimumPathLength(u, tailPos) != float('inf'):
            print "Did not run weightEnclosedSpaces"
            return path[1]
        us_id = self.you
        for snk in self.snakes: #Set weight of all possible next moves of other snakes to 0.
            if self.snakes[snk].getIdentifier() == us_id:
                ourSnake = self.snakes[snk]
                continue
            headPos = self.snakes[snk].getHeadPosition()
            headX = headPos[0]
            headY = headPos[1]
            n = []
            if (headX - 1) >= 0:
                n.append([headX-1, headY])
            if (headX + 1) < self.width:
                n.append([headX+1, headY])
            if (headY + 1) < self.height:
                n.append([headX, headY+1])
            if (headY - 1) >= 0:
                n.append([headX, headY-1])
            self.weightGrid.setWeights(n, 0)
            #self.weightGrid.showWeights(True,True)
        ourHead = ourSnake.getHeadPosition()
        path = self.weightGrid.optimumPath(ourHead, u) #Current goal
        otherOptions = []
        ourHeadX = ourHead[0]
        ourHeadY = ourHead[1]
        if (ourHeadX - 1) >= 0:
            otherOptions.append([ourHeadX-1, ourHeadY])
        if (ourHeadX + 1) < self.width:
            otherOptions.append([ourHeadX+1, ourHeadY])
        if (ourHeadY + 1) < self.height:
            otherOptions.append([ourHeadX, ourHeadY+1])
        if (ourHeadY - 1) >= 0:
            otherOptions.append([ourHeadX, ourHeadY-1])

        otherOptions.remove(path[1]) #Remove from other options our current option
        if len(ourSnake.getAllPositions()) > 1 and ourSnake.getAllPositions()[1] in otherOptions:
            otherOptions.remove(ourSnake.getAllPositions()[1]) # Remove our 'neck' from other otherOptions
        for ot in otherOptions:
            if self.weightGrid.getWeight(ot) == 0:
                otherOptions.remove(ot)
        dont = False
        for other_opt in otherOptions:
            if self.weightGrid.optimumPathLength(other_opt, u) == float('inf'):
                dont = True
        self.weightGrid.setWeights(n, 1)
        if dont:
            print "Switched directions from weightEnclosedSpaces"
            return otherOptions[0]
        return path[1]
        #set other snak eotpions to 1







        # Do not kill ourselves by picking a corner where we trap ourselves
        #TODO
            # How long are we?
            # Are we giving other people the opportunity to block off our exit?
            # What is the optimal traversal path to maximize future space opportunities
            # Don't limit our moves (against a surface) unless advantageous or necessary


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
            return 'down'
        if node[1] == (head[1] - 1):
            return 'up'
        else:
            raise ValueError('node must be adjacent')

# Example code testing
if __name__ == '__main__':
    INITDATA = {"width": 20, "height": 20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"}
    b = Game(INITDATA)
    b.weightGrid.showWeights(True, True)
    print b.getNextMove()
