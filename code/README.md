# Instructions

To test our simulation model, first ensure you have Python 2.7 and the
matplotlib and numpy Python modules installed. Then, simply execute:

```
$ python sim_batch.py
```

This will perform 1 iteration of a test simulation with 5000 pedestrians.
The number of pedestrians can easily be scaled up to the full 55,000 by simply
changing the `num_pedestrians` parameter on the last line of `sim_batch.py`.

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

# Video

Here is a video of an example simulation run:

[Video on YouTube](https://youtu.be/Zq4IOzpz85I)