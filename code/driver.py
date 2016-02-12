from grid import Grid
from simulation import Simulation

# Specify the max number of rows and columns in the grid.
max_rows = 66
max_cols = 139

# Create a type map mapping human-readable node types to integer ids.
type_map = { 'sidewalk': 1, 'crosswalk': 2, 'entrance': 3, 'exit': 4 }

# Create a grid object that contains the underlying nodes and path information.
grid = Grid(max_rows, max_cols, 'vertices.csv', 'edges.csv', type_map, 'paths.pickle')

# Set up a simulation object.
simulation = Simulation(grid, {'num_pedestrians': 500, 'visualization': True})

# Run the simulation.
simulation.run()