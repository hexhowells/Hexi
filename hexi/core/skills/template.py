# import interfaces here
import time
import sys


# entry point of skill
def start(command=None):
    pass


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
