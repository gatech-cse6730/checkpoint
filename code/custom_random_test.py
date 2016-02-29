from custom_random import CustomRandom
import numpy as np
import sys
# Import Python's random number generator, only for generating seeds for our
# own custom generator.
import random

class CustomRandomTest():
    """
    Tests a custom random number generator for use in simulation.
    """

    # Use K bins.
    K = 100

    """
    Creates a new CustomRandomTest object.

    Args:
      num_iterations: Number of iterations to perform the chi-square test.
      n_samples: Number of random number samples to collect.
      critical_value: The chi-square critical value to test against.

    Returns:
      A new CustomRandomTest object.

    """
    def __init__(self, num_iterations, n_samples, critical_value):
        self.num_iterations = num_iterations
        self.n_samples = n_samples
        self.critical_value = critical_value
        self.samples = []

    # Perform all tests.
    def test(self):
        print(("Starting tests. Performing %d iterations, please bear with "
               "us.") % self.num_iterations)

        self.perform_tests()

    def perform_tests(self):
        # Initialize a container for our failure count.
        failure_count = 0

        # Compute the expected value for each bin.
        e_i = self.n_samples / float(self.K)

        # For the number of iterations we've been given,
        for i in range(self.num_iterations):
            # Generate a histogram, segmented into K bins, containing frequencies
            # of random numbers generated with our random number generator.
            self.generate_histogram()

            # Initialize a container for our chi-square value.
            score = 0

            # Compute the chi-square value.
            for frequency in self.hist:
                score += (((frequency - e_i)**2)/e_i)

            # If our chi-square value exceeds the critical value specified,
            if score > self.critical_value:
                # Increment the failure count.
                failure_count += 1

            if i > 0 and i % 1000 == 0:
                print("---> Finished with iteration %d." % i)

        # Prepare a total failure percentage.
        total_failure = (failure_count/float(self.num_iterations))*100

        # Print the result to the user.
        print(("In %d tests, the random number generator failed to pass the "
               "chi-square test %.2f%% of the time.") % (self.num_iterations, total_failure))

    def generate_histogram(self):
        # Generate a seed for our generator using Python's random number
        # generator.
        seed = random.randrange(1, 2**31-1)
        # Initialize our random number generator.
        generator = CustomRandom(seed)

        # Clear the samples list.
        self.samples = []

        # Generate n_samples of a random number using our custom generator.
        self.samples.extend([generator.uniform_random() for i in range(self.n_samples)])

        # Prepare a histogram of the bin counts.
        self.hist = np.histogram(self.samples, bins=self.K)[0]

if __name__ == '__main__':
    # Perform the test 100,000 times.
    num_iterations = 100000

    # For each test, grab 1000 samples from our RNG.
    n_samples = 1000

    # The chi-square critical value for 99 degrees of freedom and a p-value of
    # 0.05.
    critical_value = 123.225

    # Test.
    tester = CustomRandomTest(num_iterations, n_samples, critical_value)
    tester.test()