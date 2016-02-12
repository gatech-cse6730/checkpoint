class Edge:
    """ Implementation of the edge structure in our graph. """


    """
    Creates a new edge.

    Args:
      node_a: Node.
      node_b: Node.
      weight: Float. The weight or cost of the edge.

    Returns:
      A new Edge object.

    """
    def __init__(self, node_a, node_b, weight):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight