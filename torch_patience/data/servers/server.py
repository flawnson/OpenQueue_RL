import simpy
import random

from typing import *
from logzero import logger

from torch_patience.data.patrons.patron import customer


class Queue:
    """A Simpy simulation with a class structure to mimic OpenAI's gym"""
    def __init__(self, config: Dict, render: bool = False):
        self.config = config
        self.state = {
            "prospects": 0
        }
        self.env = simpy.Environment()
        self.render_env = render
        self.counter = simpy.Resource(self.env, capacity=config["capacity"])
        self.receptionist_delay = random.uniform(config["min_delay"], config["max_delay"])  # An assigned delay
        self.curr_time_step = 1
        self.next_time_step = 2

    def _action_check(self, action):
        assert isinstance(action, int) and 0 <= action <= 6, "Illegal action by model; terminating run"

    def render(self):
        pass

    def close(self):
        pass

    def handle_prospect(self) -> Generator:
        return prospect.handle(self.env, self.counter)

    def modify_state(self, action):
        pass

    def receptionist_recovery(self):
        """Delay between receptionist service availability"""
        delay = max(self.receptionist_delay - 0.001, 0)
        yield self.env.timeout(delay)

    def init_prospect(self):
        """The initial prospects to queue up"""

        num_prospects = self.config["avg_daily_prospects"] * prospects.servicing
        for prospect in range(num_prospects):
            self.state['prospects'] += 1
            self.env.process(self.handle_prospect(inital_load=True))

    def get_observation(self):
        # Put state dictionary items into observations list
        observations = [v for k, v in self.state.items()]

        # Return starting state observations
        return observations

    def get_reward(self):
        """ Reward always negative or 0 """

        loss = None

        return loss

    def step(self, action):
        # Check if action is legal (raise exception if not):
        self._action_check(action)

        self.modify_state(action)

        self.receptionist_recovery()

        # Make a step in the simulation
        self.next_time_step += self.curr_time_step
        self.env.run(until=self.next_time_step)

        observation = self.get_observation()

        terminal = True if self.env.now >= self.sim_duration else False

        # Get reward
        reward = self._calculate_reward()

        # Information is empty dictionary (used to be compatible with OpenAI Gym)
        info = dict()

        # Render environment if requested
        if self.render_env: self.render()

        # Return tuple of observations, reward, terminal, info
        return (observation, reward, terminal, info)

    def reset(self):
        # Initialise simpy environemnt
        self.env = simpy.Environment()
        self.next_time_stop = 0

        # Set up starting processes
        self.env.process(self.handle_prospect())

        # Set starting state values
        self.state['queue_len'] = 0

        # Inital load of patients (to average occupancy)
        self.init_prospect()

        # Return starting state observations
        observations = self.get_observations()
        return observations

    def __repr__(self):
        pass

    def __str__(self):
        self.render()


