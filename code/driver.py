from grid import Grid
from simulation import Simulation

# Create a type map mapping human-readable node types to integer ids.
type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }

# Create a grid object that contains the underlying nodes and path information.
grid = Grid({
    'node_file': './map/nodes.csv',
    'edge_file': './map/edges.csv',
    'type_map': type_map,
    #'paths_file': './paths/paths_2016-02-22.pickle'
    'new_paths_file': 'paths_2016-02-27.pickle'
})

# Set up a simulation object.
simulation = Simulation(grid, {
    'num_pedestrians': 500,
    'visualization': True,
    'vis_image': './map/map.png'
})

# Run the simulation.
simulation.run()