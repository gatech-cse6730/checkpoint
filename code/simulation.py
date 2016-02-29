from printer import Printer
from pedestrian import Pedestrian
from custom_random import CustomRandom
# Python's random module is only used for generating random seeds for our own
# generator.
import random
# Numpy is used for drawing samples from a Poisson distribution for modeling
# pedestrian arrivals.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Simulation:
    """
    Performs a cellular automata simulation using an input Grid object.
    """

    CELL_WIDTH = 0.5
    PEDS_RATE = 0.81

    def __init__(self, grid, params = {}):
        self.grid = grid
        self.num_pedestrians = params.get('num_pedestrians', 500)
        self.visualization = params.get('visualization', False)
        self.vis_image = params.get('vis_image', './map/map.png')
        self.seed = params.get('seed', random.randrange(1, 2**31-1))
        self.intersection_times = params.get('intersection_times', {})

        # Initialize the random number generators.
        self.initialize_rng()

        # Create a queue of pedestrians for use in the simulation.
        self.seed_pedestrians()

    def initialize_rng(self):
        # Initialize our custom random number generator.
        self.rng = CustomRandom(self.seed)

        # Seed numpy's random number generator, for sampling from the Poisson
        # distribution.
        np.random.seed(self.seed)

    def seed_pedestrians(self):
        num_entrance_nodes = len(self.grid.entrance_nodes)
        num_destination_nodes = len(self.grid.destination_nodes)

        self.ped_queue = [self.generate_pedestrian(num_entrance_nodes, num_destination_nodes)
                          for i in range(self.num_pedestrians)]

    def generate_pedestrian(self, num_entrance_nodes, num_destination_nodes):
        entrance_node = self.grid.entrance_nodes[self.rng.random_in_range(0, num_entrance_nodes-1)]
        destination_node = self.grid.destination_nodes[self.rng.random_in_range(0, num_destination_nodes-1)]

        # TODO: set speed (third argument) dynamically by drawing from a distribution.
        new_ped = Pedestrian(entrance_node, destination_node, 1, self.grid.node_dict)

        return new_ped

    def determine_peds_per_second(self):
        total_entrance_space = len(self.grid.entrance_nodes) * self.CELL_WIDTH
        self.entry_rate = int(total_entrance_space / self.PEDS_RATE)

    # Initialize the Visualization plot.
    def init_viz(self):
        # Set interactive plot on and create figure.
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.scat = self.ax.scatter([], [], zorder=1)

        # Set background image.
        img = plt.imread(self.vis_image)
        plt.imshow(img, zorder=0)
        plt.show()

    def update_viz(self, x_vals, y_vals):
        # Clear existing points.
        self.scat.remove()

        # Update points to be plotted.
        self.scat = self.ax.scatter(x_vals, y_vals, zorder=1, color='r')

        # Draw.
        plt.draw()

        # A short pause so Mac OS X 10.11.3 doesn't break.
        plt.pause(0.0001)

    def run(self):
        Printer.pp('Initializing simulation.')

        return self.run_simulation()

    def run_simulation(self):
        self.determine_peds_per_second()

        active_peds = []

        if self.visualization:
            self.init_viz()

        timesteps = 0

        while True:
            # Initialize for viz.
            if self.visualization:
                x_vals = []
                y_vals = []

            ped_queue_length = len(self.ped_queue)

            # If our pedestrian queue is empty and we have no remaining
            # active pedestrians, break.
            if ped_queue_length == 0 and len(active_peds) == 0:
                print('Finished!')
                break

            # If there are pedestrians remaining in our queue,
            if ped_queue_length > 0:
                # Add a number of pedestrians to our SUI corresponding to our
                # computed entry rate.
                for each_ped in range(0, np.random.poisson(self.entry_rate)):
                    # If our queue is empty, break from the loop.
                    if len(self.ped_queue) == 0:
                        break

                    # Retrieve the next pedestrian in the queue.
                    next_ped = self.ped_queue[0]

                    # If her entry node is available, remove her from the queue
                    # and add her to the SUI.
                    if next_ped.current.available:
                        active_peds.append(self.ped_queue.pop(0))

            active_peds_remaining = len(active_peds)

            # Print the remaining pedestrians, and pedestrian queue count.
            if timesteps % 10 == 0:
                print(('%d active peds remaining to evacuate. Ped queue count '
                       'is %d.') % (active_peds_remaining, len(self.ped_queue)))

            # For every regular intersection
            for int_id, int_time in self.intersection_times.iteritems():
                # If intersection change time is reached
                if timesteps % int_time == 0:
                    intersection = self.grid.intersections_dict.get(int_id)
                    # Change the intersection state
                    if intersection.is_open:
                        intersection.close_me()
                    else:
                        intersection.open_me()

            # For every active pedestrian,
            for indx, ped in enumerate(active_peds):
                # If the ped is finished,
                if ped.egress_complete:
                    # Remove her.
                    del active_peds[indx]
                    continue

                # Move the ped.
                ped.move(ped.target_next, self.grid.node_dict,
                         self.grid.type_map, self.grid.neighbors_dict)

                # Get x,y values for viz.
                if self.visualization and timesteps % 100 == 0:
                    x_vals.append(ped.current.pixx)
                    y_vals.append(ped.current.pixy)

            # Update viz.
            if self.visualization and timesteps % 100 == 0:
                self.update_viz(x_vals, y_vals)

            timesteps += 1

        print('Simulation completed in %d timesteps.' % timesteps)

        if self.visualization:
            plt.close()

        return [self.seed, timesteps]
