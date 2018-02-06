from os import path


def give_path():
    return path.dirname(path.dirname(path.abspath(__file__)))
