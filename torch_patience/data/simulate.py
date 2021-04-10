""" For running simpy/gym environments sans learning model """
import argparse
import logging
import logzero
import random
import torch
import simpy
import json
import numpy as np

from typing import *
from logzero import logger

from queues.queue import Queue


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
    logger.info('Bank renege')
    random.seed(config["random_seed"])

    sim = Queue(config, render=False)

    obs = sim.setup()

    for i in range(9):
        action = np.random.choice([1, 2, 3, 4, 5])
        state_next, reward, terminal, info = sim.step(action)
        print(state_next["prospects"])
        print(len(state_next["prospects"]))
        print(reward)
        print(terminal)



