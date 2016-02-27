from shortest_path import ShortestPath

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
    def move(self, node, node_dict, type_map, neighbors_dict):
        # If the requested node is not available to move to, find a neighbor
        # of the current node that is available.
        if not node.available:
            # Initialize a found_node flag to false, that we'll update if we
            # find a node that we can move to.
            found_node = False

            # For every neighbor,
            for node_id in self.current.neighbors:
                neighbor = node_dict[node_id]

                # If the neighbor is available,
                if neighbor.available:
                    print('node not available. processing.')

                    # Set *node*, which is our target node to move to, to
                    # the neighbor.
                    node = neighbor

                    # We've found a node to move to.
                    found_node = True

                    destination_node_id = self.destination.node_id

                    # Check to see if the new node has a path to get to our
                    # destination.
                    shortest_path = node.paths.get(destination_node_id, None)

                    # If so,
                    if shortest_path:
                        # Update our shortest path to the shortest path of
                        # the node.
                        self.shortest_path = copy.deepcopy(shortest_path)

                        print('--> found shortest path. using.')
                    # If the node doesn't have a path yet computed,
                    else:
                        # Compute one.
                        shortest_path = ShortestPath(neighbors_dict,
                                                     node.node_id,
                                                     destination_node_id).path

                        # Update our shortest path.
                        self.shortest_path = shortest_path

                        # Update the node with the path.
                        node.paths[destination_node_id] = shortest_path

                        print('---> couldnt find shortest path. recomputed.')

                    # Exit the loop. We're done.
                    break

            # If we weren't able to find a node to move to,
            if not found_node:
                print('found no buddy. not moving him.')
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