import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(fileName):
    return ROOT_DIR + fileName


OUTCOMES = {"Victory", "Defeat", "Retreat"}
