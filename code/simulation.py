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

    # Define a few key constants used for generating the Poisson distribution
    # for pedestrian arrivals.
    CELL_WIDTH = 0.5
    PEDS_RATE = 0.81

    # Initialize the simulation.
    def __init__(self, grid, params = {}):
        self.grid = grid
        self.num_pedestrians = params.get('num_pedestrians', 500)
        self.visualization = params.get('visualization', False)
        self.vis_image = params.get('vis_image', './map/map.png')
        self.seed = params.get('seed', random.randrange(1, 2**31-1))
        self.intersection_times = params.get('intersection_times', {})
        self.verification_logging = params.get('verification_logging', False)

        # Initialize the random number generators.
        self.initialize_rng()

        # Create a queue of pedestrians for use in the simulation.
        self.seed_pedestrians()

        # Determine the number of peds per second that will enter the
        # simulation.
        self.determine_peds_per_second()

    # Runs the simulation.
    def run(self):
        Printer.pp('Initializing simulation.')

        return self.run_simulation()

    # Initializes the random number generator.
    def initialize_rng(self):
        # Initialize our custom random number generator.
        self.rng = CustomRandom(self.seed)

        # Seed numpy's random number generator, for sampling from the Poisson
        # distribution.
        np.random.seed(self.seed)

    # Seeds the simulation with pedestrians.
    def seed_pedestrians(self):
        # Find the number of entrance, and destination nodes.
        num_entrance_nodes = len(self.grid.entrance_nodes)
        num_destination_nodes = len(self.grid.destination_nodes)

        # Create the speed distribution used for sampling from, to give
        # each pedestrian a random speed.
        speed_distribution = self.generate_speed_distribution()

        # Create the queue of pedestrians (input stream).
        self.ped_queue = [self.generate_pedestrian(num_entrance_nodes,
                                                   num_destination_nodes,
                                                   speed_distribution)
                          for i in range(self.num_pedestrians)]

    # Generates speed distribution for sampling from (see Blue & Adler, 2001).
    def generate_speed_distribution(self):
        distribution = [2 for i in range(0, 5)]
        distribution.extend([3 for i in range(0, 90)])
        distribution.extend([4 for i in range(0, 5)])

        # Return the list, which corresponds to the distribution.
        return distribution

    # Generate a new pedestrian.
    def generate_pedestrian(self, num_entrance_nodes, num_destination_nodes, speed_distribution):
        # Select an entrance node and destination node at random.
        entrance_node = self.grid.entrance_nodes[self.rng.random_in_range(0, num_entrance_nodes-1)]
        destination_node = self.grid.destination_nodes[self.rng.random_in_range(0, num_destination_nodes-1)]

        # Select a random speed from the speed distribution.
        speed = speed_distribution[self.rng.random_in_range(0, 99)]

        # Initialize a new Pedestrian object.
        new_ped = Pedestrian(entrance_node, destination_node, speed, self.grid.node_dict)

        # Return the pedestrian.
        return new_ped

    # Determine the number of peds/s that will enter the simulation.
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

    # Update the visualization.
    def update_viz(self, x_vals, y_vals):
        # Clear existing points.
        self.scat.remove()

        # Update points to be plotted.
        self.scat = self.ax.scatter(x_vals, y_vals, zorder=1, color='r')

        # Draw.
        plt.draw()

        # A short pause so Mac OS X 10.11.3 doesn't break.
        plt.pause(0.0001)

    # Orchestrates the simulation.
    def run_simulation(self):
        # Create a list to hold active pedestrians.
        active_peds = []

        # If visualization has been selected, initialize the plot.
        if self.visualization:
            self.init_viz()

        # Create a timestep counter.
        timesteps = 0

        # If we're doing additional data collection for verification purposes,
        # initialize a list container for the data.
        if self.verification_logging:
            peds_entering_sim = []

        while True:
            # Initialize for viz.
            if self.visualization:
                x_vals = []
                y_vals = []

            if self.verification_logging:
                num_peds_entering_sim = 0

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

                    # If we're doing extra verification, log the proposed
                    # addition of the ped to the simulation.
                    if self.verification_logging:
                        num_peds_entering_sim += 1

                    # If her entry node is available, remove her from the queue
                    # and add her to the SUI.
                    if next_ped.current.available:
                        active_peds.append(self.ped_queue.pop(0))

            active_peds_remaining = len(active_peds)

            # Print the remaining pedestrians, and pedestrian queue count.
            if timesteps % 10 == 0:
                print('%d active peds remaining to evacuate. Ped queue count '
                      'is %d.' % (active_peds_remaining, len(self.ped_queue)))

            # For every regular intersection,
            for int_id, int_time in self.intersection_times.iteritems():
                # If intersection change time is reached,
                if timesteps % int_time == 0:
                    intersection = self.grid.intersections_dict.get(int_id)
                    # Change the intersection state.
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
                for i in range(0, ped.speed):
                    ped.move(ped.target_next, self.grid.node_dict,
                             self.grid.type_map, self.grid.neighbors_dict)

                # Get x,y values for viz.
                if self.visualization and timesteps % 10 == 0:
                    x_vals.append(ped.current.pixx)
                    y_vals.append(ped.current.pixy)

            # Update viz.
            if self.visualization and timesteps % 10 == 0:
                self.update_viz(x_vals, y_vals)

            # If we are doing additional verification logging, append the number
            # of peds that entered the simulation that time step to the
            # list.
            if self.verification_logging and num_peds_entering_sim > 0:
                peds_entering_sim.append(num_peds_entering_sim)

            # Increment our timesteps.
            timesteps += 1

        print('Simulation completed in %d timesteps.' % timesteps)

        # Close the plot.
        if self.visualization:
            plt.close()

        retval = [self.seed, timesteps]

        if self.verification_logging:
            retval.append(peds_entering_sim)

        return retval
