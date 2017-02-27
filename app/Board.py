"""Calculate best path and path benefits.
    Includes vertices and edges."""
import re
import igraph
import colorsys
from appJar import gui


class Board:
    """Store square weight and calculate optimal paths between them."""


    def __init__(self, size):
        """Initialize the Graph class."""

        if not isinstance(size, int):
            raise ValueError('size must be an integer')
        if size <= 1:
            raise ValueError('size must be greater than 1')

        self.size = size
        self.graph = igraph.Graph(directed=True)
        for row in range(size + 1):
            for col in range(size + 1):
                self.graph.add_vertex(name=str(row) + ',' + str(col))

        for row in range(size):
            for col in range(size):
                self.graph.add_edge(str(row) + ',' + str(col),
                                    str(row) + ',' + str(col + 1), weight=50.0)
                self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) +
                                    "," + str(col), weight=50.0)

        for row in range(1, size + 1):
            for col in range(1, size + 1):
                self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' +
                                    str(col - 1), weight=50.0)
                self.graph.add_edge(str(row) + ',' + str(col), str(row - 1) +
                                    "," + str(col), weight=50.0)


    def checkNode(self, u):
        """Check if u is a valid node."""

        match = re.match('^(\\d+),(\\d+)$', u)
        if match is None:
            raise ValueError('nodes should be in the form \'a,b\'')
        one = int(match.group(1))
        two = int(match.group(2))
        if one >= self.size or one < 0 or two >= self.size or two < 0:
            raise ValueError('node is out of bounds')


    def getSize(self):
        """Return board size"""

        return self.size


    def setWeight(self, u, weight):
        """Set incoming edges of vertex u to weight."""

        self.setWeightErrorCheck(u, weight)  # comment this out for speed

        if weight < 0:
            weight = 0
        elif weight > 100:
            weight = 100

        vertexId = self.graph.vs.find(u)
        edges = self.graph.incident(vertexId)
        for edge in edges:
            self.graph.es.find(edge)["weight"] = float(100 - weight)


    def setWeightErrorCheck(self, u, weight):
        """Check setWeight() method for errors."""

        if not isinstance(weight, int) and not isinstance(weight, float):
            raise ValueError('weight must be a number')

        self.checkNode(u)


    def multiplyWeight(self, u, multiplier):
        """Multiply weight of node u by multiplier."""

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight * multiplier)


    def divideWeight(self, u, divisor):
        """Divide weight of node u by divisor."""

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight / divisor)


    def addWeight(self, u, addend):
        """Increase weight of node u by addend."""

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight + addend)


    def subtractWeight(self, u, subtrahend):
        """Decrease weight of node u by subtrahend."""

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight - subtrahend)


    def getWeight(self, u):
        """Return the weight of the node u."""

        self.checkNode(u)  # comment this out for speed
        vertexId = self.graph.vs.find(u)
        edge = self.graph.incident(vertexId)[0]
        return 100 - self.graph.es.find(edge)["weight"]


    def optimumPath(self, u, v):
        """Return shortest path between nodes u and v."""

        self.optimumPathErrorCheck(u, v)  # comment this out for speed

        vertexIds = self.graph.get_shortest_paths(u, to=v, weights="weight",
                                             mode="OUT", output="vpath")[0]
        vertexNames = []
        for vertexId in vertexIds:
            name = self.graph.vs.find(vertexId)["name"]
            vertexNames.append(name)
        return vertexNames


    def optimumPathErrorCheck(self, u, v):
        """Check optimumPath() method for errors."""

        if u == v:
            raise ValueError('u and v cannot be the same node')

        self.checkNode(u)
        self.checkNode(v)


    def show(self, colours, numbers):
        """Visualize weights of each node"""

        self.showErrorCheck(colours, numbers)  # comment this out for speed

        app = gui('Login Window', '950x950')
        app.setBg('white')
        app.setTitle('SneakySnake Visualiser')

        for i in range(self.size):
            for k in range(self.size):

                nodeName = str(i) + "," + str(k)
                weight = self.getWeight(nodeName)

                # interpolate square value from gridValue into HSV value
                # between red and green, convert to RGB, convert to hex
                hexCode = '#%02x%02x%02x' % tuple(i * 255 for i in
                            colorsys.hls_to_rgb((weight * 1.2) /
                            float(360), 0.6, 0.8))
                if weight == 0: # color perfect non-valid entries black
                    hexCode = '#000000'
                if weight == 100: # color perfect full-valid entries blue
                    hexCode = '#2196F3'
                if weight > 100 or weight < 0: # color invalid entries grey
                    hexCode = '#616161'

                if numbers:
                    app.addLabel(nodeName, weight, i, k)
                else:
                    app.addLabel(nodeName, '', i, k)

                if colours is True:
                    app.setLabelBg(nodeName, hexCode)  # set background colour

        app.go()

    @staticmethod
    def showErrorCheck(colours, numbers):
        """Check show() method for errors."""

        if not isinstance(colours, bool):
            raise ValueError('colours must be a boolean')

        if not isinstance(numbers, bool):
            raise ValueError('numbers must be a boolean')


if __name__ == '__main__':
    g = Board(20)
    g.setWeight("1,0", 500)
    g.setWeight("1,1", 100)
    g.setWeight("19,19", -1)
    g.setWeight("19,18", 0)
    g.setWeight("10,10", 80)
    g.setWeight("10,9", 20)
    print g.optimumPath("0,0", "3,5")
    print g.getWeight("1,0")
    g.multiplyWeight("2,0", 1)
    print g.getWeight("2,0")
    #g.show(True, False)
