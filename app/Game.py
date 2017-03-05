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


        self.tauntDict = {
            'GMO':'Do you have any non-GMO food?',
            'war':'War. War never changes',
            'Slither':'Sssssslithering',
            'Snakes' : 'Snakes? I hate snakes',
            'Hungry' : 'Where can a snake get a bite to eat around here',
            'rdm':'UP'
        }

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
        if 'dead_snakes' in data:
            for deadData in data['dead_snakes']:
                if deadData['id'] in self.snakes:
                    del self.snakes[deadData['id']]
                    self.deadSnakes[deadData['id']] = deadData
                    newDead = deadData['id']

    def showBoard(self):
        """Use to show board with weight and colours """
        self.weightGrid.showWeights(True, True)


    def getNextMove(self):
        """"Use all algorithms to determine the next best move for our snake."""

        self.weightGrid.resetWeights()

        # RUN WEIGHTING ALGORITHMS HERE

        self.weightNotHitSnakes()
        self.weightFood()

        # RUN WEIGHTING ALGORITHMS HERE

        self.weightGrid.setEdges()

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
                duplicateNodes = self.weightGrid.getNodesWithPriority(priorityTarget, priorityTarget + numDuplicates - 1)
                closestLen = sys.maxint
                closestPos = []

                for node in duplicateNodes:
                    tempPath = self.weightGrid.optimumPath(usSnake.getHeadPosition(), node)
                    tempLen = len(tempPath)

                    if tempLen < closestLen and self.weightGrid.optimumPathLength(usSnake.getHeadPosition(), node) != float('inf'):
                        closestLen = tempLen
                        closestPos = node

                priorityTarget += numDuplicates

                target = closestPos

            if target == []:
                nodeValid = False
            elif self.weightGrid.optimumPathLength(usSnake.getHeadPosition(), closestPos) != float('inf'):
                nodeValid = True

        print "Following path: " + str(target)

        nextMove = self.weightEnclosedSpaces(target)
        return self.convertNodeToDirection(nextMove, self.you)

    def getTaunt(self):
        """Return taunt for the \move request"""
        nextTaunt = ''

        #If a snake died last turn, taunt them and clear the newDead variable
        if newDead != 'False':
            deadData = deadSnakes['newDead']
            nextTaunt = 'RIP '+deadData['name']+', turn 0 - turn '+self.turn-1
            newDead = 'False'
        else:
            #Create random direction
            directions = ['GOING UP', 'GOING DOWN', 'GOING LEFT', 'GOING RIGHT']
            self.tauntDict['rdm'] = random.choice(directions)
            #Pick random taunt from taunt dictionary
            nextTaunt = random.choice(self.tauntDict.items())

        return nextTaunt

    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and it self"""

        us = self.snakes[self.you] #Represents our snakes
        ourSnakePos = us.getAllPositions()
        ourTail = ourSnakePos[-1]
        ourTailX = ourTail[0]
        ourTailY = ourTail[1]

        for s in self.snakes:
            print s
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

        return self.weightGrid.optimumPath(head, self.food[closestFoodCoord])


    def weightSmallSnakes(self):
        """Positively weight smaller snakes for murdering purposes"""
        #TODO
            #Compare size
            #How long will it take to get to the snake?
            #How much food is around for the snake to grow?
        oursnake = self.snakes[self.you]
        ourSize = oursnake.Snake.getSize()
        weightAdd = 7
        for otherSnake in self.snakes:
            otherSnakeSize = self.snakes[otherSnake].Snake.getSize()
            headA = otherSnake.headArea(otherSnake)
            if  otherSnakeSize < ourSize:
                weightAdd += 8
            for headCoord in headA:
                self.weightGrid.addWeight(headCoord, weightAdd)
            #if len(self.snakes[otherSnake].weightFood()) < 3 && otherSnakeSize + 1 < ourSize:
            #instead of setWeights use addWeight to loop through each coordinate and add it
            #self.weightGrid.setWeights(self.headArea(otherSnake), )

    def headArea(self, snek):
        """Return an area around the head so that it can be weighted
        param1: snake whose head area needs to be evaluated"""

        #TODO
            #find head
            #find area
            #find body
            #return coordinates
        head = snek.Snake.getHeadPosition()
        xCoord = head[0]
        yCoord = head[1]
        newCoordinates = []
        #goes through a 4x4 grid around the snake and creates an array of those coordinates
        for xCoordNew in range(xCoord-2, xCoord+2):
            for yCoordNew in range(yCoord-2, yCoord+2):
                newCoordinates.append([xCoordNew, yCoordNew])
        #removes any body segments from the grid
        for bodySegment in snek.Snake.getAllPositions():
            newCoordinates.remove(bodySegment)
        #return new bodyless coordinates
        return newCoordinates




    def weightLargeSnakes(self):
        """Negativly weight squares where large snake heads could move to next round"""
        #TODO
            #Compare size
            #Can we get food and grow bigger?
        ourSnake = self.snakes[self.you]
        ourSize = ourSnake.Snake.getSize()
        weightSubtract = 7
        distanceToFood = ourSnake.weightFood()
        for otherSnake in self.snakes:
            otherSnakeSize = self.snakes[otherSnake].Snake.getSize()
            headA = otherSnake.headArea(otherSnake)
            if  otherSnakeSize > ourSize:
                weightSubtract += 8
            for headCoord in headA:
                self.weightGrid.subtractWeight(headCoord, weightSubtract)
            #ourSnake.weightFood()
            #otherSnake.weightFood()


    def weightEnclosedSpaces(self, u):
        us_id = self.you
        for snk in self.snakes: #Set weight of all possible next moves of other snakes to 0.
            if snk.identifier == us_id:
                ourSnake = snk
                continue
            headPos = snk.getHeadPosition()
            headX = headPos[0]
            headY = headPos[1]
            n = []
            if(headX-1>=0):
                n.append([headX-1, headY])
            if(headX+1<self.width):
                n.append([headX+1, headY])
            if(headY+1<self.height):
                n.append([headX, headY+1])
            if(headY-1>=0):
                n.append([headX, headY-1])
            self.weightGrid.setWeights(n, 0)
            #self.weightGrid.showWeights(True,True)
        ourHead = ourSnake.getHeadPosition
        path = self.weightGrid.optimumPath(ourHead, u) #Current goal
        otherOptions = []
        ourHeadX = ourHead[0]
        ourHeadY = ourHead[1]
        if(ourHeadX-1>=0):
            otherOptions.append({ourHeadX-1, ourHeadY})
        if(ourHeadX+1<self.width):
            n.append({ourHeadX+1, ourHeadY})
        if(ourHeadY+1<self.height):
            n.append({ourHeadX, ourHeadY+1})
        if(ourHeadY-1>=0):
            n.append({ourHeadX, ourHeadY-1})
        otherOptions.remove(path[1]) #Remove from other options our current option
        otherOptions.remove(ourSnake.getAllPositions[1]) # Remove our 'neck' from other otherOptions
        for ot in otherOptions:
            if(self.weightGrid.getWeight(ot) == 0):
                otherOptions.remove(ot)
        dont = False
        for other_opt in otherOptions:
            if self.weightGrid.optimumPathLength(other_opt, u) == float('inf'):
                dont = True
        if dont:
            print "Switched directions from weightEnclosedSpaces"
            return otherOptions[0]
        self.weightGrid.setWeights(n, 1)
        #set other snak eotpions to 1







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
