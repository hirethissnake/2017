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
                self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' +
                str(col + 1), weight=1)
                self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) +
                ',' + str(col), weight=1)

        print self.graph

    def shortestPath(self, u, v):
        """Return shortest path between nodes u and v."""
        return self.graph.get_shortest_paths(u, to=v, weight="weight")

    """

    isDirected()
    shortestPath(u,v)
    isPathPossible()
    addEdge()
    addVertex()
    ...etc

    """

if __name__ == '__main__':
    g = Board(20)
