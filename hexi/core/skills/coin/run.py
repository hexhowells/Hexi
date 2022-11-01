# import interfaces here
from hexi.interfaces.display import display
import random
import time


# entry point of skill
def start(command=None):
    screen = display.Display()
    coins = ["HEADS", "TAILS"]
    idx = random.randint(0, 1)
    x_pos = 15 if idx == 0 else 20
    screen.draw_text_custom(coins[idx], x_pos, 20, 28)
    time.sleep(5)


if __name__ == "__main__":
    start()
