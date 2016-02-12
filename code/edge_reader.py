from reader import Reader
from edge import Edge
import csv

class EdgeReader(Reader):
    """
    Reads in edges from a CSV input file, creating new Edge objects for each.
    Saves those edge objects to an edges list.
    """


    def __init__(self, filename):
        # Initialize an edges container.
        self.edges = []

        # Call __init__ on the parent class.
        super(EdgeReader, self).__init__(filename)

    def process(self):
        with open(self.filename, 'rb') as csvfile:
            # Skip the first line.
            next(csvfile)

            # Create a CSV reader.
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                # The node_a and node_b corresponding to node_ids.
                node_a = int(row[0])
                node_b = int(row[1])

                # The weight is a float value that will be used for computations.
                weight = float(row[2])

                # Create a new edge.
                newedge = Edge(node_a, node_b, weight)

                # Append it to the edges array.
                self.edges.append(newedge)

        return self