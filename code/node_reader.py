from reader import Reader
from node import Node
import csv

class NodeReader(Reader):
    """
    Reads in vertices from a CSV input file, creating new Node objects for each.
    Saves those node objects to a node_dict Dictionary indexed by node_id.
    """


    def __init__(self, filename):
        # Initialize a node container and a node dictionary.
        self.nodes = []
        self.node_dict = {}

        # Call __init__ on the parent class.
        super(NodeReader, self).__init__(filename)

    def process(self):
        with open(self.filename, 'rb') as csvfile:
            # Skip the first line.
            next(csvfile)

            # Create a CSV reader.
            reader = csv.reader(csvfile, delimiter=',')

            for indx, row in enumerate(reader):
                # The node_id for the Node will be indx.
                node_id = indx

                # Node type.
                node_type = int(row[6])

                # X and y coordinates.
                x = int(row[0])
                y = int(row[1])
                pixx = float(row[2])
                pixy = float(row[3])

                # Create a new node.
                newnode = Node(node_id, node_type, x, y, pixx, pixy)

                # Append it to the nodes array.
                self.nodes.append(newnode)

                # Add an entry in the node dictionary.
                self.node_dict[node_id] = newnode

        return self