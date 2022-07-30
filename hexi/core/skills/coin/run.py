# import interfaces here
from hexi.interfaces.display import display
import random
import time


# entry point of skill
def start(command=None):
    screen = display.Display()
    coins = ["heads", "tails"]
    idx = random.randint(0, 1)
    screen.draw_text(coins[idx])
    time.sleep(5)


if __name__ == "__main__":
    start()
