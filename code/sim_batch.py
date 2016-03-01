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

    def initialize_grid(self, paths_file=None):
        # Create a type map mapping human-readable node types to integer ids.
        type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }
        self.grid = None

        if paths_file == None:
            self.pickle_name = self.name + '.pickle'
            # Create a grid object that contains the underlying nodes and path information.
            self.grid = Grid({
                'node_file': './map/nodes.csv',
                'intersection_file': './map/intersections.csv',
                'closed_intersections': self.intersection_conf.get('closed'),
                'edge_file': './map/edges.csv',
                'type_map': type_map,
                'new_paths_file': self.pickle_name
            })
        else:
            self.pickle_name = paths_file
            # Create a grid object that contains the underlying nodes and path information.
            self.grid = Grid({
                'node_file': './map/nodes.csv',
                'intersection_file': './map/intersections.csv',
                'closed_intersections': self.intersection_conf.get('closed'),
                'edge_file': './map/edges.csv',
                'type_map': type_map,
                'paths_file': paths_file
            })

    def run_sims(self, params = {}):
        self.initialize_grid(params.get('paths_file', None))
        
        if not os.path.exists('./results'):
            os.makedirs('./results')
            
        self.res_file_path = './results/' + self.name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.txt'

        for run_num in range(self.num_sims):
            if run_num > 0:
                self.initialize_grid(self.pickle_name)

            simulation = Simulation(self.grid, {
                'num_pedestrians': params.get('num_pedestrians', 500),
                'visualization': params.get('visualization', False),
                'vis_image': './map/map.png',
                'intersection_times': self.intersection_times
            })

            seed, res = simulation.run()
            self.write_outputs([seed, res])

    def write_outputs(self, res):
        with open(self.res_file_path, 'a+') as res_file:
            res_file.write(str(res[0]) + ',' + str(res[1]) +'\n')

def main(argv):
    config_file = None
    num_peds = None
    vis_boolean = None
    paths_file = None
    try:
        opts, args = getopt.getopt(argv,"hc:p:v:f:",["help", "config=", "peds=", "viz=", "pfile="])
    except getopt.GetoptError:
        print 'sim_batch.py -c <configJsonFile> -p <int numPeds> -v <t/f vizBoolean> -f <pathsFile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'sim_batch.py -c <configJsonFile> -p <int numPeds> -v <t/f vizBoolean> -f <pathsFile>'
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
        elif opt in ("-f", "--pfile"):
            paths_file = arg

    if config_file == None:
        print "config file was not given (json file)"
        sys.exit(2)
    if num_peds == None:
        print "number of pedestrians was not given (integer)"
        sys.exit(2)
    if vis_boolean == None:
        print "visualization boolean was not given (t/f)"
        sys.exit(2)
    if paths_file == None:
        print "no paths file given. creating a new one for this simulation."

    sb = SimBatch(config_file)
    sb.run_sims({'num_pedestrians': num_peds, 'visualization': vis_boolean, 'paths_file': paths_file})

if __name__ == '__main__':
    main(sys.argv[1:])
