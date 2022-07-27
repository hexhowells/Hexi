from random import randrange
from hexi.interfaces.display import display


def init_stars(num_stars, max_depth):
    stars = []
    for i in range(num_stars):
        # A star is represented as a list with this format: [X,Y,Z]
        star = [randrange(-25, 25), randrange(-25, 25), randrange(1, max_depth)]
        stars.append(star)
    return stars


def move_and_draw_stars(screen, stars, max_depth):
    origin_x = screen.width // 2
    origin_y = screen.height // 2

    renders = []

    for star in stars:
        # The Z component is decreased on each frame.
        star[2] -= 0.19

        # If the star has past the screen then reposition it far away from the screen
        if star[2] <= 0:
            star[0] = randrange(-25, 25)
            star[1] = randrange(-25, 25)
            star[2] = max_depth

        # Convert the 3D coordinates to 2D using perspective projection.
        k = 128.0 / star[2]
        x = int(star[0] * k + origin_x)
        y = int(star[1] * k + origin_y)

        # Draw the star (if it is visible in the screen).
        if 0 <= x < screen.width and 0 <= y < screen.height:
            size = (1 - float(star[2]) / max_depth) * 4
            renders.append((x, y, size, size))

    screen.draw_rectangles(renders)


def start_animation():
    max_depth = 32
    stars = init_stars(512, max_depth)
    screen = display.Display()
    
    while True:
        move_and_draw_stars(screen, stars, max_depth)


if __name__ == "__main__":
        start_animation()

