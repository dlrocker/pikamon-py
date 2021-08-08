import os
import json
import logging
import logging.config

LOGGING_CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../configuration/logging.json"


def hello(s):
    logging.info("Hello {}".format(s))


if __name__ == "__main__":
    with open(LOGGING_CONFIG_FILE, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    hello("world!")
