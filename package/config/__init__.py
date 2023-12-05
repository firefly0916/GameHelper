import logging
import os
from pathlib import Path

PROJECT_DIR = str(Path(__file__).resolve().parents[2])


class ArgsStarRail(object):
    def __init__(self):
        self.img_dir = os.path.join(PROJECT_DIR, "package", "starrail", "image")


class Config(object):
    def __init__(self):
        self.args_star_rail = ArgsStarRail()


def set_logger():
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


if __name__ == "__main__":
    print(ArgsStarRail().img_dir)
