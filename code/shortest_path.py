# Dijkstra's algorithm for shortest paths.
# Implementation adapted from online version published by David Eppstein, UC Irvine, 4 April 2002.
# Accessible at https://www.ics.uci.edu/~eppstein/161/python/dijkstra.py.
from priodict import priorityDictionary

class ShortestPath:
    """ An abstraction for finding the shortest path between two nodes in a graph. """


    """
    Creates a new ShortestPath instance.

    Args:
      graph: Dictionary. Should be a dictionary with keys corresponding to each node_id
        in the graph. Each key should itself point to another dictionary, with keys corresponding
        to neighboring nodes, and values corresponding to edge weights.
      start: Integer. The node_id of the starting node.
      end: Integer: The node_id of the destination node.

    Returns:
      A new ShortestPath object.

    """
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start = start
        self.end = end

        # Generate the shortest path from the given start to the destination.
        self.path = self.generate_shortest_path(self.graph, self.start, self.end)

    # Returns the next node in the shortest path.
    # def next_node(self):
    #     try:
    #         shortest_path = self.shortest_path(self.graph, self.start, self.end)
    #     except Exception:
    #         return None
    #
    #     return shortest_path[1]

    # Implements Dijkstra's algorithm, given a graph G, start node_id, and end node_id.
    def dijkstra(self, G, start, end=None):
        """
        Find shortest paths from the  start vertex to all vertices nearer than or equal to the end.

        The input graph G is assumed to have the following representation:
        A vertex can be any object that can be used as an index into a dictionary.
        G is a dictionary, indexed by vertices.  For any vertex v, G[v] is itself a dictionary,
        indexed by the neighbors of v.  For any edge v->w, G[v][w] is the length of the edge.
        This is related to the representation in <http://www.python.org/doc/essays/graphs.html>
        where Guido van Rossum suggests representing graphs as dictionaries mapping vertices
        to lists of outgoing edges, however dictionaries of edges have many advantages over lists:
        they can store extra information (here, the lengths), they support fast existence tests,
        and they allow easy modification of the graph structure by edge insertion and removal.
        Such modifications are not needed here but are important in many other graph algorithms.
        Since dictionaries obey iterator protocol, a graph represented as described here could
        be handed without modification to an algorithm expecting Guido's graph representation.

        Of course, G and G[v] need not be actual Python dict objects, they can be any other
        type of object that obeys dict protocol, for instance one could use a wrapper in which vertices
        are URLs of web pages and a call to G[v] loads the web page and finds its outgoing links.

        The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is the
        predecessor of v along the shortest path from s to v.

        Dijkstra's algorithm is only guaranteed to work correctly when all edge lengths are positive.
        This code does not verify this property for all edges (only the edges examined until the end
        vertex is reached), but will correctly compute shortest paths even for some graphs with negative
        edges, and will raise an exception if it discovers that a negative edge has caused it to make a mistake.
        """

        D = {}	# dictionary of final distances
        P = {}	# dictionary of predecessors
        Q = priorityDictionary()	# estimated distances of non-final vertices
        Q[start] = 0

        for v in Q:
            D[v] = Q[v]
            if v == end: break

            for w in G[v]:
                vwLength = D[v] + G[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError, "Dijkstra: found better path to already-final vertex"
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

        return (D,P)

    # Finds the shortest path given a graph G, start node_id, and end node_id.
    def generate_shortest_path(self, G, start, end):
        """
        Find a single shortest path from the given start vertex to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along the shortest path.
        """

        D,P = self.dijkstra(G,start,end)
        Path = []
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
        Path.reverse()
        return Path