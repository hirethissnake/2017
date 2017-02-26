"""Calculate best path and path benefits.
    Includes vertices and edges."""
import igraph

class Board:

    def __init__(self, size):
        """Initialize the Graph class"""

        self.graph = igraph.Graph(directed=True)
        for row in range(size + 1):
            for col in range(size + 1):
                self.graph.add_vertex(name=str(row) + ',' + str(col))

        for row in range(size):
            for col in range(size):
                self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' + str(col + 1), weight=0)
                self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) + ',' + str(col))

        print self.graph

	def shortestPath(u, v):
		print test

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
