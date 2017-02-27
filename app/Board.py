"""Calculate best path and path benefits.
    Includes vertices and edges."""
import re
import igraph


class Board:
    """Store square weight and calculate optimal paths between them."""


    def __init__(self, size):
        """Initialize the Graph class."""

        self.size = size
        self.graph = igraph.Graph(directed=True)
        for row in range(size + 1):
            for col in range(size + 1):
                self.graph.add_vertex(name=str(row) + ',' + str(col))

        for row in range(size):
            for col in range(size):
                self.graph.add_edge(str(row) + ',' + str(col),
                                    str(row) + ',' + str(col + 1), weight=1)
                self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) +
                                    "," + str(col), weight=1)

        for row in range(1, size + 1):
            for col in range(1, size + 1):
                self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' +
                                    str(col - 1), weight=1)
                self.graph.add_edge(str(row) + ',' + str(col), str(row - 1) +
                                    "," + str(col), weight=1)


    def isNode(self, u):
        """Check if u is a valid node"""

        match = re.match('^(\\d+),(\\d+)$', u)
        if match is None:
            raise ValueError('nodes should be in the form \'a,b\'')
        one = int(match.group(1))
        two = int(match.group(2))
        if one >= self.size or one < 0 or two >= self.size or two < 0:
            raise ValueError('node is out of bounds')


    def optimumPath(self, u, v):
        """Return shortest path between nodes u and v."""

        self.optimumPathErrorCheck(u, v)  #comment this out for speed

        vertexIds = self.graph.get_shortest_paths(u, to=v, weights="weight",
                                             mode="OUT", output="vpath")[0]
        vertexNames = []
        for vertexId in vertexIds:
            vertexNames.append(self.graph.vs.find(vertexId)["name"])
        return vertexNames


    def optimumPathErrorCheck(self, u, v):
        """Check optimumPath() method for errors"""

        if u == v:
            raise ValueError('u and v cannot be the same node')

        self.isNode(u)
        self.isNode(v)


    def setWeight(self, u, weight):
        """Set incoming edges of vertex u to weight"""

        self.setWeightErrorCheck(u, weight)  #comment this out for speed

        if weight < 0:
            weight = 0
        elif weight > 100:
            weight = 100

        edges = self.graph.incident(self.graph.vs.find(u))
        for edge in edges:
            self.graph.es.find(edge)["weight"] = 100 - weight


    def setWeightErrorCheck(self, u, weight):
        """Check setWeight() method for errors"""

        if not isinstance(weight, int) and not isinstance(weight, float):
            raise ValueError('weight must be a number')

        self.isNode(u)


if __name__ == '__main__':
    g = Board(20)
    g.setWeight("1,5", 10)
    print g.optimumPath("0,0", "0,a")
