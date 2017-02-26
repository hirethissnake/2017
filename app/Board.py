"""Calculate best path and path benefits.
    Includes vertices and edges."""
import igraph


class Board:
    """Store square weight and calculate optimal paths between them."""

    def __init__(self, size):
        """Initialize the Graph class."""

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

        """shortest = self.shortestPath("0,1", "2,5")

        print self.graph
        print shortest
        for vertex in shortest:
            print self.graph.vs.find(vertex)"""

    def optimumPath(self, u, v):
        """Return shortest path between nodes u and v."""
        return self.graph.get_shortest_paths(u, to=v, weights="weight",
                                             mode="OUT", output="vpath")[0]

    def setWeight(self, u, weight):
        """Set incoming edges of vertex u to weight"""
        edges = self.graph.incident(self.graph.vs.find(u))
        for edge in edges:
            self.graph.es.find(edge)["weight"] = weight
        print self.graph.es["weight"]


if __name__ == '__main__':
    """Run code in this class for testing"""
    g = Board(20)
    g.setWeight("1,1", 2)
