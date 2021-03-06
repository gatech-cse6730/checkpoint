# Usage Instructions

To test our simulation model, first ensure you have Python 2.7 and the
matplotlib and NumPy Python modules installed. Then, simply execute:

```
$ python sim_batch.py -c config/config1.json -p 5000 -v t -f paths/config1.pickle
```

This will run 20 5,000-pedestrian simulations based on configuration 1, which is
defined in `config/config1.json`.

To see the general format for running our simulation program, simply run:
```
$ python sim_batch.py -h
```

There are a few key command line options that can be passed to `sim_batch.py`,
which is the primary interface to our model:

* `-c`: JSON configuration file. Defines intersections to be kept open for
pedestrians, closed, or managed by traffic cops.
* `-p`: Integer. Number of pedestrians for each simulation.
* `-v`: Boolean (t/f). Whether or not to enable visualization (this launches
a matplotlib plot which shows pedestrian progress through the simulation).
* `-f`: Pickle paths file. File containing precomputed shortest paths for each
entrance node in the simulation, to every possible destination node using
Dijkstra's algorithm.

The output will initially state that a preprocessing step is being performed
to prepare the simulation. Then, the actual simulation will begin. Pedestrians
will be created and will begin moving toward their destinations. As
they do, the number of "active pedestrians" remaining in the SUI will be
displayed at every time step, as well as the number of pedestrians remaining in
the queue (in other words, those who haven't yet entered the SUI). Once the
simulation has finished, the number of time-steps required to evacuate the SUI
will be shown.

The results of the simulations will also be logged to a file in the `results`
subdirectory. Each line in a results file corresponds to a
`<random_seed, number_of_timesteps>` pair for a particular simulation.

# Random number generator

To test the random number generator, simply execute:

```
$ python custom_random_test.py
```

This will perform 100,000 iterations of a test procedure in which 1000 samples
are drawn from our custom generator. It will compute the chi-square statistic
for each test and compare it with the critical value, and at the end of the test
procedure will print the percentage of failures.

# Video

Here is a video of an example simulation run:

[Video on YouTube](https://youtu.be/k2iQPcyWEF8)