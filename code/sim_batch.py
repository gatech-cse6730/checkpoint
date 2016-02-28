import json
import os
import datetime
from grid import Grid
from simulation import Simulation

import pprint
pp = pprint.PrettyPrinter(indent=4)

class SimBatch:
    def __init__(self, config_path):
        # dict with list of 'open' and 'closed' intersection ids
        self.intersection_conf = {}
        # dict with time for intersections to open and close
        self.intersection_time = {}
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
                    self.intersection_time[int(x.get('id'))] = int(x.get('time'))

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
        simulation = Simulation(self.grid, {
            'num_pedestrians': params.get('num_pedestrians', 500),
            'visualization': params.get('visualization', 500),
            'vis_image': './map/map.png'
        })
        self.results = []
        for run_num in range(self.num_sims):
            res = simulation.run()
            self.results.append(res)
        self.write_outputs()

    def write_outputs(self):
        if not os.path.exists('./results'):
            os.makedirs('./results')
        res_file_path = './results/' + self.name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.txt'

        with open(res_file_path, 'w') as res_file:
            for res in self.results:
                res_file.write(str(res) +'\n')

sb = SimBatch('./config/noclosed.json')
sb.run_sims({'num_pedestrians': 1, 'visualization': True})
