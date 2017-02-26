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


    def optimumPath(self, u, v):
        """Return shortest path between nodes u and v."""
        vertexIds = self.graph.get_shortest_paths(u, to=v, weights="weight",
                                             mode="OUT", output="vpath")[0]
        vertexNames = []
        for vertexId in vertexIds:
            vertexNames.append(self.graph.vs.find(vertexId)["name"])
        return vertexNames


    def setWeight(self, u, weight):
        """Set incoming edges of vertex u to weight"""

        if not isinstance(weight, int) and not isinstance(weight, float):
            raise ValueError('Weight must be a number')
        if weight < 0:
            weight = 0
        elif weight > 100:
            weight = 100

        match = re.match('^(\\d+),(\\d+)$', u)
        if match.group(0) >= self.size or match.group(0) < 0 or match.group(1) \
          >= self.size or match.group(1) < 0:
            raise ValueError('node u is invalid')

        edges = self.graph.incident(self.graph.vs.find(u))
        for edge in edges:
            self.graph.es.find(edge)["weight"] = 100 - weight


if __name__ == '__main__':
    g = Board(20)
    g.setWeight("0,1", 10)
    g.setWeight("1,1", 10)
    g.setWeight("2,1", 10)
    print g.optimumPath("0,0", "2,5")
