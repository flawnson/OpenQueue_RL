import random
import simpy

from typing import *
from logzero import logger


RANDOM_SEED = 42
NEW_CUSTOMERS = 25  # Total number of customers
INTERVAL_CUSTOMERS = 5.0  # Generate new customers roughly every x seconds


# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)  # Exponential distribution
        yield env.timeout(t)

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()  # NOT running until no more events to process, run until next time step





