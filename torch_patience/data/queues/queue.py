import simpy
import names  # To get random name for prospects
import random

from typing import *
from logzero import logger

from patrons.prospect import AbstractProspect, Prospect


class Queue:
    """A Simpy simulation with a class structure to mimic OpenAI's gym"""
    def __init__(self, config: Dict, render: bool = False):
        self.config = config
        self.env_config = config["env_config"]
        self.state = {
            "prospects": []  # A list of prospective patrons
        }
        self.render_env = render
        self.env = simpy.Environment()
        self.counter = simpy.Resource(self.env, capacity=self.env_config["max_capacity"])  # capacity is line capacity
        self.receptionist_delay = random.uniform(self.env_config["min_delay"], self.env_config["max_delay"])  # An assigned delay
        self.template_prospect = AbstractProspect(config, self.env)
        self.curr_time_step = 1
        self.next_time_step = 1

    def _action_check(self, action):
        assert 0 <= action <= 6, f"{action} is an illegal action by model; terminating run"

    def render(self):
        pass

    def close(self):
        pass

    def handle_new_prospect(self, new_prospect) -> Generator:
        return new_prospect.handle(self.counter)

    def modify_state(self, action):
        pass

    def receptionist_recovery(self):
        """Delay between receptionist service availability"""
        delay = max(self.receptionist_delay - 0.001, 0)
        yield self.env.timeout(delay)

    def init_prospects(self):
        """The initial prospects to queue up"""

        num_prospects = self.env_config["mean_daily_prospects"] * self.template_prospect.servicing
        for prospect in range(num_prospects):
            new_prospect = Prospect(self.config, names.get_full_name(), self.env)
            self.state["prospects"].append(new_prospect)
            self.env.process(self.handle_new_prospect(new_prospect))

    def get_observations(self):
        # Put state dictionary items into observations list
        # Consider adding len(counter.users) a.k.a counter.count
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

        observation = self.get_observations()

        terminal = True if self.env.now >= self.env_config["duration"] else False

        # Get reward
        reward = self.get_reward()

        # Information is empty dictionary (used to be compatible with OpenAI Gym)
        info = dict()

        # Render environment if requested
        if self.render_env: self.render()

        # Return tuple of observations, reward, terminal, info
        return (observation, reward, terminal, info)

    def reset(self):
        # Initialise simpy environment
        # self.env = simpy.Environment()
        self.next_time_step = 0

        # Initial load of patients (to average occupancy)
        self.init_prospects()

        # # Set up starting processes
        # self.env.process(self.handle_new_prospect())

        # Set starting state values
        self.state["prospects"].clear()

        # Return starting state observations
        observations = self.get_observations()
        return observations

    def __repr__(self):
        pass

    def __str__(self):
        self.render()


