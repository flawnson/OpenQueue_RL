import random

from typing import *
from logzero import logger


DEFAULT_MIN_PATIENCE = 1  # Min. customer patience
DEFAULT_MAX_PATIENCE = 3  # Max. customer patience


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    logger.info('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(DEFAULT_MIN_PATIENCE, DEFAULT_MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            logger.info('%7.4f %s: Waited, %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            logger.info('%7.4f %s: Finished, %6.3f' % (env.now, name, tib))

        else:
            # We reneged
            logger.info('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


class Prospect:
    def __init__(self, config, id, env):
        self.id = id  # A UID (probably just a name for now)
        self.config = config  # Config dict from JSON file
        self.patience = random.uniform(config["min_patience"], config["max_patience"])  # An assigned patience
        self.servicing = random.uniform(config["min_servicing"], config["max_servicing"])  # An assigned service time
        self.arrival = env.now  # The time the prospective customer is instantiated

    def render(self):
        pass

    def handle(self, env, counter):
        with counter.request() as req:
            # Wait for the counter or abort at the end of our tether
            results = yield req | env.timeout(self.patience)

            wait = env.now - self.arrival  # The time the prospective customer is instantiated to the current time

            if req in results:
                tib = random.expovariate(1.0 / self.servicing)  # NOT ACTUALLY PATIENCE (NEED TO UNDERSTAND AND FIX)

                yield env.timeout(self.servicing)

            else:
                logger.info(f"{env.now} {self.name}: RENEGED after {wait}")

    def write(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        self.render()




