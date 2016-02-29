from node_reader import NodeReader
from edge_reader import EdgeReader
from intersection_reader import IntersectionReader
from printer import Printer
from shortest_path import ShortestPath

import pickle

class Grid:
    """
    Builds a grid used for translating the graph into a meaningful 2D arrangement.
    """


    def __init__(self, params = {}):
        # Save some important attributes.
        self.node_file = params['node_file']
        self.intersection_file = params['intersection_file']
        self.closed_intersections = params['closed_intersections']
        self.edge_file = params['edge_file']
        self.type_map = params['type_map']
        self.paths_file = params.get('paths_file', None)
        self.new_paths_file = params.get('new_paths_file', None)

        # Perform initialization of the gridspace.
        self.initialize_nodes()
        self.initialize_intersections()
        self.initialize_edges()
        self.set_paths()

    def initialize_nodes(self):
        reader = NodeReader(self.node_file)

        # Save the node dict for later lookups.
        self.node_dict = reader.node_dict

        # Save off the node array.
        self.nodes = reader.nodes

        # Initialize a list container of entrance nodes.
        self.entrance_nodes = []

        # Initialize a list container of destination nodes.
        self.destination_nodes = []

        # Iterate through the returned nodes,
        for node in self.nodes:
            # If the node is an entrance node, add it to the entrance nodes list.
            if node.node_type == self.type_map['entrance']:
                self.entrance_nodes.append(node)
            # If the node is an exit node, add it to the exit nodes list.
            elif node.node_type == self.type_map['exit']:
                self.destination_nodes.append(node)

    def initialize_intersections(self):
        reader = IntersectionReader(self.intersection_file, self.node_dict)

        self.intersections_dict = reader.intersections_dict
        self.intersections = reader.intersections
        for int_id in self.closed_intersections:
            nodes_list = self.intersections_dict.get(int_id).nodes
            for node in nodes_list:
                del self.node_dict[node.node_id]
            del self.intersections_dict[int_id]

    def initialize_edges(self):
        reader = EdgeReader(self.edge_file)

        # Save off the edges array.
        edges = reader.edges

        for edge in edges:
            # Look up the first node.
            node_a = self.node_dict.get(edge.node_a)

            # Look up the second node to make sure it exists.
            node_b = self.node_dict.get(edge.node_b)

            if node_a is not None and node_b is not None:
                # Add a new entry to node a's neighbors dict for node b, setting it
                # to the weight.
                node_a.neighbors[node_b.node_id] = edge.weight

                # Added to make undirected.
                node_b.neighbors[node_a.node_id] = edge.weight

        # Initialize a dictionary to store just the neighbors.
        self.neighbors_dict = {}

        # For every entry in the node dictionary,
        for node_id, node_obj in self.node_dict.iteritems():
            # Save just the neighbors.
            self.neighbors_dict[node_id] = node_obj.neighbors

    def set_paths(self):
        # If we already have an existing file containing the paths data in
        # pickle format, read it in and update the paths attributes on our
        # nodes.
        if self.paths_file:
            # Load the data.
            with open(self.paths_file, 'rb') as f:
                paths_data = pickle.load(f)

                for node in self.entrance_nodes:
                    data_for_node = paths_data.get(node.node_id, None)

                    if data_for_node:
                        node.paths = data_for_node

        else:
            # Initialize a paths container that we will write to a file.
            paths_dict = {}

            Printer.pp('Performing preprocessing step to find shortest paths. Please bear with us.')

            num_nodes = len(self.entrance_nodes)

            # Iterate through every entrance node, updating the *paths*
            # dictionary attribute to include the shortest path to every
            # destination node.
            for indx, node in enumerate(self.entrance_nodes):
                node_id = node.node_id

                # Compute the paths for every possible destination.
                for destination in self.destination_nodes:
                    destination_node_id = destination.node_id

                    node.paths[destination_node_id] = ShortestPath(self.neighbors_dict,
                                                                   node_id,
                                                                   destination_node_id).path

                paths_dict[node_id] = node.paths

                percent_done = ((indx+1)/float(num_nodes))*100
                print('%.2f percent done.' % percent_done)

            # If we've specified a file to write our shortest paths to,
            if self.new_paths_file:
                # Write the paths to a file.
                with open(self.new_paths_file, 'wb') as f:
                    pickle.dump(paths_dict, f, -1)

                print('---> Dumped paths to %s.' % self.new_paths_file)

        print('---> Preprocessing done.')
