from reader import Reader
from intersection import Intersection
import csv

class IntersectionReader(Reader):
    """ Processes intersections for use in the parametric simulation. """

    def __init__(self, filename, node_dict):
        # Initialize an intersection container and an intersection dictionary.
        self.intersections = []
        self.intersections_dict = {}
        self.node_dict = node_dict

        # Call __init__ on the parent class.
        super(IntersectionReader, self).__init__(filename)

    def process(self):
        with open(self.filename, 'rb') as csvfile:
            # Skip the first line.
            next(csvfile)

            # Create a CSV reader.
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                int_id = int(row[0]) #intersection id
                node_id = int(row[1]) #node id

                if self.intersections_dict.get(int_id) is not None:
                    # if intersection already exists, append node to it
                    cur_int = self.intersections_dict.get(int_id)
                    cur_int.nodes.append(self.node_dict.get(node_id))
                else:
                    # otherwise, create new intersection with the node
                    new_int =  Intersection(int_id, [self.node_dict.get(node_id)])
                    # Append it to the intersection array.
                    self.intersections.append(new_int)
                    # Add an entry in the intersection dictionary.
                    self.intersections_dict[int_id] = new_int

        return self
