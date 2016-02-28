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


    def __init__(self, grid, params = {}):
        self.grid = grid
        self.num_pedestrians = params.get('num_pedestrians', 500)
        self.visualization = params.get('visualization', False)
        self.vis_image = params.get('vis_image', 'playMat.png')
        self.seed = params.get('seed', random.randrange(1, 2**31-1))

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
        active_peds = []

        if self.visualization:
            self.init_viz()

        timesteps = 0
        while True:
            # Initialize for viz.
            if self.visualization:
                x_vals = []
                y_vals = []

            target_next_dict = {node: [] for node in self.grid.nodes}

            if len(self.ped_queue) == 0 and len(active_peds) == 0:
                print('Finished!')
                break

            if len(self.ped_queue) > 0:
                next_ped = self.ped_queue[0]

                if next_ped.current.available:
                    active_peds.append(self.ped_queue.pop(0))

            active_peds_remaining = len(active_peds)

            if active_peds_remaining % 10 == 0:
                print('%d active peds remaining to evacuate.' % active_peds_remaining)

            for indx, ped in enumerate(active_peds):
                # If the ped is finished,
                if ped.egress_complete:
                    # Remove her.
                    del active_peds[indx]
                    continue

                # Grab the ped's target next node according to the shortest path algo.
                target_next = ped.target_next

                # Add an entry in the node => peds dictionary, telling us that the ped
                # wants to go to that node.
                target_next_dict[target_next].append(ped)

                # Get x,y values for viz.
                if self.visualization:
                    x_vals.append(ped.current.pixx)
                    y_vals.append(ped.current.pixy)

            for node, peds in target_next_dict.iteritems():
                ped_len = len(peds)

                if ped_len == 0:
                    # No pedestrian wants the node, so go to the next iteration.
                    continue
                elif ped_len == 1:
                    # We're done; only one ped wants the node.
                    ped = peds[0]
                else:
                    # Select a ped at random to get the node.
                    ped = peds[self.rng.random_in_range(0, ped_len-1)]

                # Move the ped.
                ped.move(node, self.grid.node_dict, self.grid.type_map,
                         self.grid.neighbors_dict)

            # Update viz.
            if self.visualization:
                self.update_viz(x_vals, y_vals)

            timesteps += 1

        print('Simulation completed in %d timesteps.' % timesteps)

        if self.visualization:
            plt.close()

        return timesteps
