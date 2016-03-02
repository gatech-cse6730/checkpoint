import json
import os
import datetime
import sys
import getopt
import json
from grid import Grid
from simulation import Simulation

import pprint
pp = pprint.PrettyPrinter(indent=4)

class SimBatch:
    """
    Handles batch-running of multiple simulations.
    """

    # Initialize a SimBatch.
    def __init__(self, config_path):
        # Dict with list of 'open' and 'closed' intersection ids.
        self.intersection_conf = {}

        # Dict with time for intersections to open and close.
        self.intersection_times = {}

        # Read in the config file at the given path.
        self.config_path = config_path
        self.read_config(config_path)

    # Reads a given configuration file.
    def read_config(self, config_path):
        with open(config_path) as config_json:
            config = json.load(config_json)

        self.name = config.get('name')
        self.num_sims = int(config.get('num_sims'))

        # Iterates through the given parameters, preparing the data for use
        # in managing the simulation.
        for param in config.get('parameters'):
            p_type = param.get('type')
            if p_type == 'intersection_closed':
                self.intersection_conf['closed'] = [int(x) for x in param.get('data').get('intersections')]
            elif p_type == 'intersection_open':
                self.intersection_conf['open'] = [int(x) for x in param.get('data').get('intersections')]
            elif p_type == 'intersection_normal':
                for x in (param.get('data').get('intersections')):
                    self.intersection_times[int(x.get('id'))] = int(x.get('time'))

    # Initialize the underyling grid (i.e., graph) structure that will be used
    # in the simulation.
    def initialize_grid(self, paths_file = None):
        # Create a type map mapping human-readable node types to integer ids.
        type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }
        self.grid = None

        # Creates a new grid given a paths file.
        def create_grid(paths_file = None, new_paths_file = None):
            opts = {
                'node_file': './map/nodes.csv',
                'intersection_file': './map/intersections.csv',
                'closed_intersections': self.intersection_conf.get('closed'),
                'edge_file': './map/edges.csv',
                'type_map': type_map,
            }

            if paths_file:
                opts['paths_file'] = paths_file

            if new_paths_file:
                opts['new_paths_file'] = new_paths_file

            self.grid = Grid(opts)

        # If no paths file has been given to us, create one.
        if paths_file == None:
            # Create a grid object that contains the underlying nodes and path
            # information.
            self.pickle_name = self.name + '.pickle'
            create_grid(None, self.pickle_name)
        # If we have been given a paths file, use it.
        else:
            # Create a grid object that contains the underlying nodes and path
            # information.
            self.pickle_name = paths_file
            create_grid(self.pickle_name, None)

    # Performs the key step - running of multiple simulations.
    def run_sims(self, params = {}):
        # Initialize the grid.
        self.initialize_grid(params.get('paths_file', None))

        # Determine whether we are doing extra logging for verification
        # purposes.
        verification_logging = params.get('verification_logging', False)

        # If so, and no directory for holding verification results has been
        # created, create one.
        if verification_logging and not os.path.exists('./verification'):
            os.makedirs('./verification')

        # Create a directory for holding results if none exists yet.
        if not os.path.exists('./results'):
            os.makedirs('./results')

        # Determine the file path for our results file.
        self.res_file_path = self.filename_with_time('./results/', self.name, '.txt')

        # For each iteration in the given number of simulations,
        for run_num in range(self.num_sims):
            # Initialize our grid if it hasn't been already.
            if run_num > 0:
                self.initialize_grid(self.pickle_name)

            # Create a simulation object.
            simulation = Simulation(self.grid, {
                'num_pedestrians': params.get('num_pedestrians', 500),
                'visualization': params.get('visualization', False),
                'vis_image': './map/map.png',
                'intersection_times': self.intersection_times,
                'verification_logging': verification_logging
            })

            # Do additional logging if necessary.
            if verification_logging:
                seed, res, ped_distribution = simulation.run()
                # Write outputs to our results file.
                self.write_outputs(seed, res, ped_distribution)
            else:
                seed, res = simulation.run()
                # Write outputs to our results file.
                self.write_outputs(seed, res)

    # Writes simulation outputs to a results file.
    def write_outputs(self, seed, res, ped_distribution = None):
        if ped_distribution:
            ped_dist_path = self.filename_with_time('./verification/',
                                                    self.name, '.json')

            with open(ped_dist_path, 'w') as outfile:
                json.dump(ped_distribution, outfile)

        with open(self.res_file_path, 'a+') as res_file:
            write_string = str(seed) + ',' + str(res) + '\n'
            res_file.write(write_string)

    # Builds a filename including a timestamp.
    def filename_with_time(self, dirname, filename, ext):
        def time_now():
            return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        return dirname + filename + '_' + time_now() + ext

def main(argv):
    # Initialize some parameters.
    config_file = None
    num_peds = None
    vis_boolean = False
    paths_file = None
    verification_logging = False

    help_message = ('sim_batch.py -c <configJsonFile> -p <int numPeds> '
                    '-v <t/f vizBoolean> -f <pathsFile> '
                    '-V <t/f verificationBoolean>')

    # Retrieve command line arguments.
    try:
        opts, args = getopt.getopt(argv,'hc:p:v:f:V:',['help', 'config=',
                                                      'peds=', 'viz=', 'pfile=',
                                                      'verify='])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    # Process command line arguments.
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ('-c', '--config'):
            config_file = arg
        elif opt in ('-p', '--peds'):
            num_peds = int(arg)
        elif opt in ('-v', '--viz'):
            if arg == 't' or arg == 'T':
                vis_boolean = True
            else:
                vis_boolean = False
        elif opt in ('-f', '--pfile'):
            paths_file = arg
        elif opt in ('-V', '--verify'):
            if arg == 't' or arg == 'T':
                verification_logging = True
            else:
                verification_logging = False

    if config_file == None:
        print 'config file was not given (json file)'
        sys.exit(2)

    if num_peds == None:
        print 'number of pedestrians was not given (integer)'
        sys.exit(2)

    if vis_boolean == None:
        print 'visualization boolean was not given (t/f)'
        sys.exit(2)

    if paths_file == None:
        print 'no paths file given. creating a new one for this simulation.'

    # Initialize a new SimBatch.
    sb = SimBatch(config_file)

    # Set some opts for our SimBatch.
    sim_opts = {
        'num_pedestrians': num_peds,
        'visualization': vis_boolean,
        'paths_file': paths_file,
        'verification_logging': verification_logging
    }

    # Run the simulations.
    sb.run_sims()

if __name__ == '__main__':
    main(sys.argv[1:])