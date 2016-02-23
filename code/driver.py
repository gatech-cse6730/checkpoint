from grid import Grid
from simulation import Simulation

# Create a type map mapping human-readable node types to integer ids.
type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }

# Create a grid object that contains the underlying nodes and path information.
grid = Grid({
    'node_file': 'nodes.csv',
    'edge_file': 'edges.csv',
    'type_map': type_map,
    'paths_file': 'paths_gatech.pickle'
    #'new_paths_file': 'paths_gatech.pickle'
})

# Set up a simulation object.
simulation = Simulation(grid, {
    'num_pedestrians': 500,
    'visualization': True,
    'vis_image': 'map.png'
})

# Run the simulation.
simulation.run()
