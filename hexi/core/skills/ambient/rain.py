import random
from hexi.interfaces.display import display
from hexi.interfaces.button import Button

rain_width = 1


def get_first_rain():
    raindrops = []

    for i in range(10):
        x = random.randint(0,127)
        y = random.randint(0, 60)
        length = random.randint(4, 7)
        raindrops.append((x, y, length, rain_width))

    return raindrops


def spawn_new_drops(threshold=5):
    new_drops = []
    for _ in range(3):
        if random.randint(1, 10) > threshold:
            rand_x = random.randint(0, 127)
            rand_len = random.randint(4, 7)
            y = 1 - rand_len
            new_drops.append((rand_x, y, rand_len, rain_width))

    return new_drops



def progress_rain(raindrops):
    new_raindrops = []
    for (x, y, l, w) in raindrops:
        y += random.randint(3, 5)
        if y < 64:
            new_raindrops.append((x, y, l, rain_width))
        elif l != 1:  # if raindrop isnt splash animation
            new_raindrops.append((x, 63, 1, 1))
            new_raindrops.append((x-1, 62, 1, 1))
            new_raindrops.append((x+1, 62, 1, 1))


    new_drops = spawn_new_drops()
    if len(new_drops) > 1:
        [new_raindrops.append(rain_data) for rain_data in new_drops]

    return new_raindrops


def render_drops(screen, raindrops):
    rain = [(x, y, l, w) for (x, y, l, w) in raindrops]
    screen.draw_rectangles(rain)


def start_animation():
    screen = display.Display()
    raindrops = get_first_rain()
    button = Button()

    while not button.pushed():
        render_drops(screen, raindrops)
        raindrops = progress_rain(raindrops)


if __name__ == "__main__":
    start_animation()
