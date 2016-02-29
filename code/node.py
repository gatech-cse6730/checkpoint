class Node:
    """ Implementation of the node structure in our graph. """


    """
    Creates a new node.

    Args:
      node_id: Integer.
      node_type: Integer. One of 1, 2, 3, or 4, corresponding to 'sidewalk',
          'road', 'entrance', and 'exit', respectively.
      x: Integer. The x-coordinate of the node in the grid.
      y: Integer. The y-coordinate of the node in the grid.

    Returns:
      A new Node object.

    """
    def __init__(self, node_id, node_type, x, y, pixx, pixy):
        # A unique identifier for the node.
        self.node_id = node_id

        # The node type.
        self.node_type = node_type

        # X and y coordinates for the node in the grid.
        self.x = x
        self.y = y

        # Pixel-space x and y coordinates, for plotting on top of the map.
        self.pixx = pixx
        self.pixy = pixy

        # Initialize a dictionary to hold the next node in the shortest path
        # for each destination.
        self.paths = {}

        # List of Node neighbors.
        self.neighbors = {}

        # By default, the node is not occupied (i.e., it is available).
        self.available = True

    # For a given destination node, returns the next node in the shortest path.
    def get_next_node(self, dest, node_dict):
        next_node_id = self.paths[dest.node_id]

        return node_dict[next_node_id]