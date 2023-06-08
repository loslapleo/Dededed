from os import preadv
from PIL import Image
from colorthief import ColorThief
import numpy as np

PALETTE_SIZE = 6

def apply_ordered_dithering(image_name:str, n:int):
    image = np.array(Image.open(image_name))
    palette = ColorThief(image_name).get_palette(color_count = PALETTE_SIZE)
    tm = threshold_map(n)
    new_image = Image.fromarray(ordered_dither(image, tm, n, palette), "RGB")
    new_image.save("out/new_image.png")

def threshold_map(n:int):
    if n == 1:
        return np.array([[0]])
    else:
        e1 = (n ** 2) * threshold_map(int(n / 2))
        e2 = (n ** 2) * threshold_map(int(n / 2)) + 2
        e3 = (n ** 2) * threshold_map(int(n / 2)) + 3
        e4 = (n ** 2) * threshold_map(int(n / 2)) + 1
        c1 = np.concatenate((e1, e3), axis = 0)
        c2 = np.concatenate((e2, e4), axis = 0)
        return (1 / n ** 2) * np.concatenate((c1, c2), axis = 1)

def ordered_dither(image_arr:np.array, tm:np.array, n:int, palette):
    x_max = np.size(image_arr, axis = 1)
    y_max = np.size(image_arr, axis = 0)
    for x in range(x_max):
        for y in range(y_max):
            prev_col = image_arr[y][x]
            image_arr[y][x] = get_nearest_colour(image_arr[y][x] + \
                    255 / PALETTE_SIZE * (tm[x % n][y % n]) - 0.5, palette)
            # print("%s -> %s (x:%d, y:%d)\r" % (prev_col, image_arr[y][x], x, y))
    return image_arr

def get_nearest_colour(color, palette):
    """
    Gets the nearest colour from color palette to apply to the image array.
    """
    palette = np.array(palette)
    distances = np.sqrt(np.sum((palette - color) ** 2, axis = 0))
    nearest_index = np.where(distances == np.amin(distances))
    nearest_color = palette[nearest_index]
    print("%s -> %s" % (color, nearest_color[0]))
    return nearest_color
