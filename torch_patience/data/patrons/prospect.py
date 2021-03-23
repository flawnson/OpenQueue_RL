import random

from typing import *
from logzero import logger


DEFAULT_MIN_PATIENCE = 1  # Min. customer patience
DEFAULT_MAX_PATIENCE = 3  # Max. customer patience


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
                tib = random.expovariate(1.0 / self.servicing)

                yield env.timeout(self.servicing)

            else:
                logger.info(f"{env.now} {self.name}: RENEGED after {wait}")

    def write(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        self.render()




