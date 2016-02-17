import copy

class Pedestrian:
    """ Implements a pedestrian. """


    """
    Creates a new pedestrian.

    Args:
      current: Node. A Node object corresponding to the current location of the
        pedestrian.
      destination: Node. A Node object corresponding to the destination node.
      speed: Integer. Number of grid cells traversed per time step.
      node_dict: Dictionary. Lookup table of node_id -> node object for every node
        in the simulation.

    Returns:
      A new Pedestrian object.

    """
    def __init__(self, current, destination, speed, node_dict):
        # The current location of the pedestrian, as a Node.
        self.current = current

        if not self.current.node_type == 3:
            raise ValueError('The initializing node is not an exit.')

        # The pedestrian's final destination, as a Node.
        self.destination = destination

        # The speed of the pedestrian, formulated as an integer number of
        # grid cells traversed per time step.
        self.speed = speed

        # Store the pedestrian's shortest path to his destination, as determined
        # by Dijkstra's algorithm.
        self.shortest_path = copy.deepcopy(self.current.paths[self.destination.node_id])

        # Initialize the desired next node to move to in the shortest path,
        # also known as the target next.
        self.shortest_path.pop(0)
        self.target_next = node_dict[self.shortest_path.pop(0)]

        # Whether the pedestrian has completed egress (i.e., exited the SUI).
        self.egress_complete = False

    # Move the pedestrian to a given node. Takes a node (Node), node_dict (Dictionary),
    # and type_map (Dictionary) translating string node types to node_type ids.
    def move(self, node, node_dict, type_map):
        # If the requested node is not available to move to, return.
        if not node.available:
            return

        # The current node is now available.
        self.current.available = True

        # Update the current node to the new node.
        self.current = node

        # If current is a destination node,
        if self.current.node_type == type_map['exit']:
            # Egress is completed.
            self.egress_complete = True
        else:
            # Set the new current node to unavailable.
            self.current.available = False

            # Update the target next.
            self.target_next = node_dict[self.shortest_path.pop(0)]

        return self