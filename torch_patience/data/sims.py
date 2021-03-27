""" For running simpy/gym environments sans learning model """
import argparse
import logging
import logzero
import random
import torch
import simpy
import json

from typing import *
from logzero import logger


MIN_PATIENCE, MAX_PATIENCE = 0, 10


if __name__ == "__main__":
    ### Configuring ###
    parser = argparse.ArgumentParser(description="Config file parser")
    parser.add_argument("-c", "--config", help="json config file", type=str)
    parser.add_argument("-s", "--scheme", help="json scheme file", type=str)
    args = parser.parse_args()

    config: dict = json.load(open(args.config))
    device = torch.device("cuda" if config["device"] == "cuda" and torch.cuda.is_available() else "cpu")
    logzero.loglevel(eval(config["logging"]))

    # Setup and start the simulation
    print('Bank renege')
    random.seed(config["random_seed"])
    env = simpy.Environment()


    def customer(env, name, counter, time_in_bank):
        """Customer arrives, is served and leaves."""
        arrive = env.now
        print('%7.4f %s: Here I am' % (arrive, name))
        print(counter.queue)
        print(counter.put_queue)
        print(counter.get_queue)
        print(counter.users)
        print(counter.count)

        with counter.request() as req:
            patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
            # Wait for the counter or abort at the end of our tether
            results = yield req | env.timeout(patience)

            wait = env.now - arrive

            if req in results:
                # We got to the counter
                print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

                tib = random.expovariate(1.0 / time_in_bank)
                yield env.timeout(tib)
                print('%7.4f %s: Finished' % (env.now, name))

            else:
                # We reneged
                print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


    def source(env, number, interval, counter):
        """Source generates customers randomly"""
        for i in range(number):
            c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
            env.process(c)
            t = random.expovariate(1.0 / interval)  # Exponential distribution
            yield env.timeout(t)

    # Start processes and run
    counter = simpy.Resource(env, capacity=3)
    env.process(source(env, config["patron_config"]["num_patrons"], config["patron_config"]["intervals"], counter))
    env.run()  # NOT running until no more events to process, run until next time step
