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
        self.servicing = random.randint(self.prospect_config["min_servicing"], self.prospect_config["max_servicing"])  # An assigned service time
        self.arrival = env.now  # The time the prospective customer is instantiated


class Prospect(AbstractProspect):
    def __init__(self, config, id, env):
        super(Prospect, self).__init__(config, env)
        self.id = id  # A UID (probably just a name for now)
        self.env = env
        self.config = config  # Config dict from JSON file
        self.prospect_config = config["prospect_config"]
        self.patience = random.uniform(self.prospect_config["min_patience"],
                                       self.prospect_config["max_patience"])  # An assigned patience
        self.servicing = random.expovariate(1.0 / random.randint(self.prospect_config["min_servicing"],
                                                                 self.prospect_config["max_servicing"]))  # An assigned service time
        self.arrival = env.now  # The time the prospective customer is instantiated

    def render(self):
        pass

    def handle(self, state, counter):
        with counter.request() as req:
            # Wait for the counter or abort at the end of our tether
            results = yield req | self.env.timeout(self.patience)

            wait = self.env.now - self.arrival  # The time the prospective customer is instantiated to the current time

            if req in results:
                logger.info(f"{self.env.now} {self.id}: SERVICED after {wait}")
                logger.info(len(state["prospects"]))
                state["prospects"].remove(self.id)
                yield self.env.timeout(self.servicing)

            else:
                logger.info(f"{self.env.now} {self.id}: RENEGED after {wait}")
                state["prospects"].remove(self.id)
                logger.info(len(state["prospects"]))

    def write(self):
        pass

    def __eq__(self, other):
        # Currently set to index by prospect name
        return self.id == other

    def __repr__(self):
        return f"'Name': {self.id}," \
               f"'Arrival': {self.arrival}," \
               f"'Patience': {self.patience}," \
               f"'Servicing': {self.servicing}"

    def __str__(self):
        self.render()




