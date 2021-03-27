import random

from abc import ABC, abstractmethod
from typing import *
from logzero import logger



DEFAULT_MIN_PATIENCE = 1  # Min. customer patience
DEFAULT_MAX_PATIENCE = 3  # Max. customer patience


class AbstractProspect(ABC):
    def __init__(self, config, env):
        super(AbstractProspect, self).__init__()
        self.config = config
        self.prospect_config = config["prospect_config"]
        self.patience = random.uniform(self.prospect_config["min_patience"], self.prospect_config["max_patience"])  # An assigned patience
        self.servicing = random.uniform(self.prospect_config["min_servicing"], self.prospect_config["max_servicing"])  # An assigned service time
        self.arrival = env.now  # The time the prospective customer is instantiated


class Prospect(AbstractProspect):
    def __init__(self, config, id, env):
        super(Prospect, self).__init__(config, env)
        self.id = id  # A UID (probably just a name for now)
        self.config = config  # Config dict from JSON file
        self.prospect_config = config["prospect_config"]
        self.patience = random.uniform(self.prospect_config["min_patience"], self.prospect_config["max_patience"])  # An assigned patience
        self.servicing = random.uniform(self.prospect_config["min_servicing"], self.prospect_config["max_servicing"])  # An assigned service time
        self.arrival = env.now  # The time the prospective customer is instantiated

    def render(self):
        pass

    def handle(self, env, counter):
        with counter.request() as req:
            # Wait for the counter or abort at the end of our tether
            results = yield req | env.timeout(self.patience)
            print(req)

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




