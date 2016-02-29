class Intersection:
    """
    Implements an intersection, used for parametrically limiting pedestrian flow.
    Note: the intersection is not yet used in this initial model, but its definition
        is provided here.
    """


    """
    Creates a new intersection.

    Args:
      int_id: Integer. Unique numerical identifier for the intersection.
      nodes: List. List of Node objects that are part of the intersection.

    Returns:
      A new Intersection object.

    """
    def __init__(self, int_id, nodes=[]):
        # Unique identifier.
        self.int_id = int_id
        # List of nodes that are in the intersection
        self.nodes = nodes
        # State of whether the intersection is available to pedestrians (default - closed to peds).
        self.is_open = False

    # Close all the nodes in the intersection.
    def close_me(self):
        # Need to handle case when pedestrian is in the middle of an intersection during closing.
        for node in self.nodes:
            node.available = False
        self.is_open = False

    # Re-open the intersection by setting all included & empty nodes to available.
    def open_me(self):
        for node in self.nodes:
            if node.current_ped is None:
                node.available = True
        self.is_open = True
