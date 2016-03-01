import json
import os
import datetime
import sys
import getopt
from grid import Grid
from simulation import Simulation

import pprint
pp = pprint.PrettyPrinter(indent=4)

class SimBatch:
    def __init__(self, config_path):
        # dict with list of 'open' and 'closed' intersection ids
        self.intersection_conf = {}
        # dict with time for intersections to open and close
        self.intersection_times = {}
        self.config_path = config_path

        self.read_config(config_path)
        self.initialize_grid()

    def read_config(self, config_path):
        with open(config_path) as config_json:
            config = json.load(config_json)

        self.name = config.get('name')
        self.num_sims = int(config.get('num_sims'))

        for param in config.get('parameters'):
            p_type = param.get('type')
            if p_type == 'intersection_closed':
                self.intersection_conf['closed'] = [int(x) for x in param.get('data').get('intersections')]
            elif p_type == 'intersection_open':
                self.intersection_conf['open'] = [int(x) for x in param.get('data').get('intersections')]
            elif p_type == 'intersection_normal':
                for x in (param.get('data').get('intersections')):
                    self.intersection_times[int(x.get('id'))] = int(x.get('time'))

    def initialize_grid(self):
        # Create a type map mapping human-readable node types to integer ids.
        type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }

        # Create a grid object that contains the underlying nodes and path information.
        self.grid = Grid({
            'node_file': './map/nodes.csv',
            'intersection_file': './map/intersections.csv',
            'closed_intersections': self.intersection_conf.get('closed'),
            'edge_file': './map/edges.csv',
            'type_map': type_map,
            'paths_file': './paths/paths_2016-02-22.pickle'
            #'new_paths_file': 'paths_gatech.pickle'
        })

    def run_sims(self, params = {}):
        if not os.path.exists('./results'):
            os.makedirs('./results')
        
        self.res_file_path = './results/' + self.name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.txt'

        for run_num in range(self.num_sims):
            simulation = Simulation(self.grid, {
                'num_pedestrians': params.get('num_pedestrians', 500),
                'visualization': params.get('visualization', False),
                'vis_image': './map/map.png',
                'intersection_times': self.intersection_times
            })

            # Get the results from the run - both the random number seed used, and the 
            # number of timesteps.
            seed, res = simulation.run()
            
            # Write the results to a file.
            self.write_outputs([seed, res])
            
    def write_outputs(self, res):
        with open(self.res_file_path, 'w') as res_file:
            res_file.write(str(res[0]) + ',' + str(res[1]) +'\n')
                
def main(argv):
    config_file = None
    num_peds = None
    vis_boolean = None
    try:
        opts, args = getopt.getopt(argv,"hc:p:v:",["help", "config=", "peds=", "viz="])
    except getopt.GetoptError:
        print 'sim_batch.py -c <configJsonFile> -p <int numPeds> -v <t/f vizBoolean>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'sim_batch.py -c <configJsonFile> -p <int numPeds> -v <t/f vizBoolean>'
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg
        elif opt in ("-p", "--peds"):
            num_peds = int(arg)
        elif opt in ("-v", "--viz"):
            if arg == "t" or arg == "T":
                vis_boolean = True
            else:
                vis_boolean = False

    if config_file == None:
        print "config file was not given (json file)"
        sys.exit(2)
    if num_peds == None:
        print "number of pedestrians was not given (integer)"
        sys.exit(2)
    if vis_boolean == None:
        print "visualization boolean was not given (t/f)"
        sys.exit(2)

    sb = SimBatch(config_file)
    sb.run_sims({'num_pedestrians': num_peds, 'visualization': vis_boolean})

if __name__ == '__main__':
    main(sys.argv[1:])
