"""
Calculate best path and path benefits.
Includes vertices and edges.
"""

import colorsys
import igraph
try:
    from appJar import gui
    print 'Importing appJar'
except ImportError:
    print 'Did not import appJar'
from sortedcollections import ValueSortedDict


class Board:
    """
    Store square weight and calculate optimal paths between them.

    Has the following public methods:

## OPERATORS ##     ## RETURN ##

__init__                void        Board initialization
averageWeights          void        Balance weight values using heat equation
modifyWeights           void        Operate on array of vertexes by array of
                                        weights (parent for next four functions)
multiplyWeight          void        Multiply weight of node by multiplier
divideWeight            void        Divide weight of node by divisor
addWeight               void        Increase weight of node by addend
subtractWeight          void        Decrease weight of ndoe by subtrahend

## GETTERS ##

getNodeWithPriority     [x,y]       Return vertex name with priority of some value
getNodesWithPriority    [[x, y]]    Return array of vertexes with priority
                                        between start and end
getSize                 [int, int]  Get board size as an x, y array
getWeight               int/float   Return the weight of a node u
isNodeWeightUnique      boolean     Check if node weight exists in board twice
countNodeWeightCopies   int         Get the number of copies a specific weight
optimumPath             [[x, y]]    Get the best path between two nodes

## SETTERS ##

setWeight               void        Set incoming edges of vertex u to some
                                        weight
setWeights              void        Set incoming edges of array of vertexes to
                                        matching weight in array

## DISPLAY ##
showWeights             void        Opens visualiation of weights of all nodes
showPath                void        Display graphic of best path between nodes
    """


    def __init__(self, width, height):
        """
        Initialize the Graph class.

        param1: integer - width of board
        param2: integer - height of board
        """

        self.initErrorCheck(width, height)  # comment this out for speed

        self.width = width  # declare size of board
        self.height = height

        self.graph = igraph.Graph(directed=True)  # declare graph
        for row in range(height):  # create vertices
            for col in range(width):
                self.graph.add_vertex(name=str(row) + ',' + str(col))

        for row in range(height):  # create 1/2 edges
            for col in range(width):
                if col < self.width - 1:
                    self.graph.add_edge(str(row) + ',' + str(col),
                                        str(row) + ',' + str(col + 1), weight=50.0)
                if col > 0:
                    self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' +
                                        str(col - 1), weight=50.0)
                if row < self.height - 1:
                    self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) +
                                        ',' + str(col), weight=50.0)
                if row > 0:
                    self.graph.add_edge(str(row) + ',' + str(col), str(row - 1) +
                                        ',' + str(col), weight=50.0)

        self.dictionary = ValueSortedDict()
        for row in range(height):  # populate dictionary
            for col in range(width):
                self.dictionary[str(row) + ',' + str(col)] = 50.0

        self.edges = dict()
        for row in range(height):  # save edges incident to each vertex
            for col in range(width):
                vertexId = self.graph.vs.find(str(row) + ',' + str(col))
                edges = self.graph.incident(vertexId) # list of edges
                edges = [self.graph.es.find(edge) for edge in edges]
                self.edges[str(row) + ',' + str(col)] = edges


    def initErrorCheck(self, width, height):
        """
        Check init() for errors.

        param1: integer - width to check
        param2: integer - height to check
        """

        self.checkInt(width)
        self.checkInt(height)

        if width <= 1:
            raise ValueError('width must be greater than 1')
        if height <= 1:
            raise ValueError('height must be greater than 1')


    @staticmethod
    def nodeAsString(u):
        """
        Return a node as a string

        param1: [[x, y]] - node to convert
        return: string - node representation
        """

        return str(u[0]) + ',' + str(u[1])


    @staticmethod
    def stringAsNode(u):
        """
        Return a string as a node

        param1: [int, int] - node in form [x, y]
        return: [[x, y]] - node representation
        """

        coords = u.split(',')
        return [int(coords[0]), int(coords[1])]


    def checkNode(self, u):
        """
        Check if u is a valid node.

        param1: [int, int] - node in the form [x, y]
        """

        if len(u) != 2:
            raise ValueError('nodes should be in the form [x, y]')
        if u[0] >= self.height or u[0] < 0 or u[1] >= self.width or u[1] < 0:
            raise ValueError('node is out of bounds')


    @staticmethod
    def checkNumber(num):
        """
        Check if num is an integer/float.

        param1: unknown - item to confirm if integer/float
        """

        if not isinstance(num, int) and not isinstance(num, float):
            raise ValueError('number must be an integer/float')


    @staticmethod
    def checkInt(num):
        """
        Check if num is an integer.

        param1: unknown - item to confirm if integer
        """

        if not isinstance(num, int):
            raise ValueError('number must be an integer')


    def getSize(self):
        """
        Return board size.

        return: [integer] - array with [width, height]
        """

        return [self.width, self.height]


    def setWeight(self, u, weight):
        """
        Set incoming edges of vertex u to weight.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - weight to set
        """

        self.modifyWeightErrorCheck(u, weight)  # comment this out for speed

        if weight <= 0:  # ensure weight is in bounds
            weight = float("-inf")  # do not visit under any circumstances
        elif weight > 100:
            weight = float(100)

        nodeName = self.nodeAsString(u)

        self.dictionary[nodeName] = 100 - float(weight)  # ensure front is highest


    def resetWeights(self):
        """
        Reset all weights to 50.
        """

        for key in self.dictionary:
            self.dictionary[key] = 50.0


    def setEdges(self):
        """
        Set edge weights from dictionary.
        """
        for node in self.dictionary:
            weight = self.dictionary[node]
            for edge in self.edges[node]:  # 100 - weight is to unsure higher weights
                                        # correlate to shorter paths when traversing
                edge['weight'] = float(weight)


    def setWeights(self, nodes, value):
        """
        Modify a list of node weights.

        param1: [[int, int]] - array of nodes in the form [<integer>,<integer>]
        param2: float/int - weight to set
        """

        tempLen = len(nodes)

        for nodeIndex in range(tempLen):
            self.setWeight(nodes[nodeIndex], value)


    def modifyWeights(self, operator, nodes, value):
        """
        Modify a list of node weights.

        param1: string - operator ('*', '/', '+', '-')
        param2: [[int, int]] - array of nodes in the form <integer>,<integer>
        param3: float/int - value to modify by
        """

        self.modifyWeightsErrorCheck(operator)  # comment speed

        tempLen = len(nodes)

        for nodeIndex in range(tempLen):
            if operator == "*":
                self.multiplyWeight(nodes[nodeIndex], value)
            elif operator == "/":
                self.divideWeight(nodes[nodeIndex], value)
            elif operator == "+":
                self.addWeight(nodes[nodeIndex], value)
            elif operator == "-":
                self.subtractWeight(nodes[nodeIndex], value)


    @staticmethod
    def modifyWeightsErrorCheck(operator):
        """
        Check modifyWeights() method for errors.

        param1: string - operator to check
        """

        if operator != '*' and operator != '/' and operator != '+' \
                    and operator != '-':
            raise ValueError('invalid operator')


    def multiplyWeight(self, u, multiplier):
        """
        Multiply weight of node u by multiplier.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to multiply weight by
        """

        self.modifyWeightErrorCheck(u, multiplier)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight * multiplier)


    def divideWeight(self, u, divisor):
        """
        Divide weight of node u by divisor.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to divide weight by
        """

        self.modifyWeightErrorCheck(u, divisor)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight / divisor)


    def addWeight(self, u, addend):
        """
        Increase weight of node u by addend.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to add to weight
        """

        self.modifyWeightErrorCheck(u, addend)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight + addend)


    def subtractWeight(self, u, subtrahend):
        """
        Decrease weight of node u by subtrahend.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to subtract from weight
        """

        self.modifyWeightErrorCheck(u, subtrahend)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight - subtrahend)


    def modifyWeightErrorCheck(self, u, num):
        """
        Check weight modification method for errors.

        param1: unknown - item to confirm if node
        param2: unknown - item to confirm if integer/float
        """

        self.checkNode(u)
        self.checkNumber(num)


    def getWeight(self, u):
        """
        Return the weight of the node u from the dictionary.

        param1: [int, int] - node in the form [x, y]
        return: integer/float - weight of node u
        """

        self.checkNode(u)  # comment this out for speed

        weight = 100 - self.dictionary[self.nodeAsString(u)]
        if weight == -float('inf'):
            weight = 0

        return weight  # allow human-readable


    def averageWeights(self, iterations):
        """
        Balance weight values using heat equation.

        param1: int - number of iterations to perform
        """

        toReset = []
        gridOld = []
        for row in range(self.height):  # loop through every node
            tempRow = []
            for col in range(self.width):
                currentWeight = self.getWeight([row, col])
                tempRow.append(currentWeight)
                if currentWeight != 50:
                    toReset.append([row, col])
            gridOld.append(tempRow)

        while iterations > 0:  # average grid iterations times
            tempGrid = []
            for row in range(self.height):  # loop through every node
                tempRow = []
                for col in range(self.width):
                    currentWeight = gridOld[row][col]
                    if [row, col] not in toReset:
                        toAverage = []
                        if row > 0:  #store surrounding nodes
                            toAverage.append([row - 1, col])
                        if row < self.height - 1:
                            toAverage.append([row + 1, col])
                        if col > 0:
                            toAverage.append([row, col - 1])
                        if col < self.width - 1:
                            toAverage.append([row, col + 1])

                        tempSum = currentWeight
                        count = 1
                        for node in toAverage:  # sum weights
                            tempWeight = gridOld[node[0]][node[1]]
                            if tempWeight != 50:
                                tempSum += tempWeight
                                count += 1
                        average = float(tempSum / count)
                        tempRow.append(average)
                    else:
                        tempRow.append(currentWeight)

                tempGrid.append(tempRow)
            gridOld = tempGrid
            iterations -= 1  # decrement counter

        for row in range(self.height):  # add weights back to graph
            for col in range(self.width):
                self.setWeight([row, col], gridOld[row][col])


    def getNodeWithPriority(self, index):
        """
        Return vertex name with priority index.

        param1: int - index to return priority (can be negative)
        return: [int, int] - node name with priority index
        """

        self.checkInt(index)  # comment this out for speed

        nodeString = self.dictionary.iloc[index]
        return [int(x) for x in nodeString.split(',')]


    def getNodesWithPriority(self, start, end):
        """
        Return vertex name with priority index.

        param1: int - start index to return priority
        param2: int - end index to return priority
        return: [[int, int]] - node names with priority from start-end
        """

        self.getNodesWithPriorityErrorCheck(start, end)  # comment for speed

        nodesString = self.dictionary.iloc[start : end + 1]
        nodesArray = [self.stringAsNode(x) for x in nodesString]

        return nodesArray


    def getNodesWithPriorityErrorCheck(self, start, end):
        """
        Check getNodesWithPriority() for errors.

        param1: int - start index to return priority
        param2: int - end index to return priority
        """

        self.checkInt(start)
        self.checkInt(end)


    def isNodeWeightUnique(self, u):
        """
        Return False if weight appears more than once in the graph.

        param1: [int, int] - node in the form [x, y]
        return: boolean - True if weight is unique, Fale otherwise
        """

        if self.countNodeWeightCopies(u) > 1:
            return False
        return True


    def countNodeWeightCopies(self, u):
        """
        Return False if weight appears more than once in the graph.

        param1: [int, int] - node in the form [x, y]
        return: int - Returns number of other nodes with same weight
        """

        self.checkNode(u)  # comment this out for speed

        targetWeight = 100 - self.getWeight(u)
        return self.dictionary.values().count(targetWeight)  # occurrences


    def optimumPath(self, u, v):
        """
        Return shortest path between nodes u and v.

        param1,2: [int, int] - node in the form [x, y]
        return: [[int, int]] - node names in the optimum path from u to v
        """

        self.optimumPathErrorCheck(u, v)  # comment this out for speed

        ids = self.graph.get_shortest_paths(self.nodeAsString(u),
                                                  to=self.nodeAsString(v),
                                                  weights='weight', mode='IN',
                                                  output='vpath')[0]
                                             # generate list of Ids in path
        return [self.stringAsNode(self.graph.vs.find(x)['name']) for x in ids]


    def optimumPathErrorCheck(self, u, v):
        """
        Check optimumPath() method for errors.

        param1,2: unknown - item to confirm if node
        """

        if u == v:
            raise ValueError('u and v cannot be the same node')

        self.checkNode(u)
        self.checkNode(v)


    def optimumPathLength(self, u, v):
        """
        Return length of optimal path between 2 nodes.

        param1,2: [int, int] - node in the form [x, y]
        return: float - length of path
        """

        return self.graph.shortest_paths(self.nodeAsString(u),
                                         self.nodeAsString(v), \
                                         'weight', 'IN')[0][0]


    def showWeights(self, colours, numbers):
        """
        Visualize weights of each node.

        param1: boolean - show colours on display?
        param2: boolean - show numbers on display?
        """

        self.showWeightsErrorCheck(colours, numbers)  # comment for speed

        self.showCombiner([], colours, numbers)


    @staticmethod
    def showWeightsErrorCheck(colours, numbers):
        """
        Check showWeights() method for errors.

        param1,2: unknown - item to check if boolean
        """

        if not isinstance(colours, bool):
            raise ValueError('colours must be a boolean')

        if not isinstance(numbers, bool):
            raise ValueError('numbers must be a boolean')


    def showPath(self, u, v):
        """
        Visualize path between nodes u and v.

        param1,2: [int, int] - node in the form [x, y]
        """

        self.optimumPathErrorCheck(u, v)  # comment this out for speed

        self.showCombiner(self.optimumPath(u, v), True, True)


    def showCombiner(self, pathValues, colours, numbers):
        """
        Visualize weights of each node.

        param1: array - path nodes to colour
        param1: boolean - show colours on display?
        param2: boolean - show numbers on display?
        """

        app = gui('Login Window', '950x950')
        app.setBg('white')
        app.setTitle('SneakySnake Visualiser')

        for row in range(self.height):
            for col in range(self.width):

                nodeName = str(row) + ',' + str(col)
                weight = self.getWeight([row, col])

                # interpolate square value from gridValue into HSV value
                # between red and green, convert to RGB, convert to hex
                hexCode = '#%02x%02x%02x' % tuple(i * 255 for i in
                            colorsys.hls_to_rgb((weight * 1.2) /
                            float(360), 0.6, 0.8))
                if weight == 0: # color perfect non-valid entries black
                    hexCode = '#000000'
                if weight == 100: # color perfect full-valid entries blue
                    hexCode = '#0033cc'
                if weight > 100 or (weight != float('-inf') and weight < 0):
                    # color invalid entries grey
                    hexCode = '#616161'
                if [row, col] in pathValues:
                    # color path values cyan
                    hexCode = '#66ffff'

                if numbers: # add numbers
                    app.addLabel(nodeName, "%.2f" % weight, col, row)
                else:
                    app.addLabel(nodeName, '', col, row)

                if colours is True: # add colours
                    app.setLabelBg(nodeName, hexCode)

        app.go() # show window


    def printDict(self):
        """
        Print dictionary.
        """

        print self.dictionary



if __name__ == '__main__':
    g = Board(20, 20)
    g.setWeights([[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]], 0)
    g.setEdges()
    print g.optimumPath([3, 3], [1, 1])
    print g.optimumPathLength([3, 3], [1, 1]) == float("inf")
    g.showWeights(True, True)
    """g.setWeight([0, 5], 0)
    g.setWeight([1, 5], 0)
    g.setWeight([2, 5], 0)
    g.setWeight([3, 5], 0)
    g.setWeight([1, 3], 99.9)
    g.setWeight([4, 5], 100)
    g.setWeights([[1, 1], [2, 1]], [0.2, 0.2])
    print g.optimumPath([0, 0], [6, 4])
    #print g.getNodesWithPriority(0, 1)
    #print g.isNodeWeightUnique([0, 2])
    #print g.countNodeWeightCopies([2, 2])
    #g.showWeights(True, False)
    #print g.getWeight([0, 1])
    #g.multiplyWeight([2, 0], 1)
    #print g.getWeight([2, 0])
    #g.sortNames()
    #print g.dictionary
    #g.show(True, True)
    print g.getWeight([3, 5])
    print g.getNodeWithPriority(0)
    print g.getNodesWithPriority(0, 1)
    #g.showWeights(True, True)
    g.averageWeights(20)
    g.showPath([0, 0], [0, 10])
    #g.showWeights(True, True)"""
    #print g.optimumPath([11, 7], [0, 0])
    #print g.graph
