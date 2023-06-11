from PIL import Image
import numpy as np
import progress_bar

def apply(image_name:str, n:int = 4, nc:int = 8):
    image_arr = np.array(Image.open(image_name), dtype = float) / 255
    tm = threshold_map(n)
    new_image = Image.fromarray(ordered_dither(image_arr, tm, n, nc))
    new_image.save("out/o_dithering.png")

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

def ordered_dither(image_arr, tm, n:int, nc):
    x_max = np.size(image_arr, axis = 1)
    y_max = np.size(image_arr, axis = 0)
    for x in range(x_max):
        for y in range(y_max):
            image_arr[y][x] = get_nearest_colour(image_arr[y][x].copy() + \
                    nc * (tm[y % n][x % n] - 0.5), nc)
        progress_bar.print_progress_bar(x, x_max, prefix = "Ordered        ", \
                length = 64)
    progress_bar.print_progress_bar(1, 1, prefix = "Ordered        ", length = 64)
    carr = np.array(image_arr / np.max(image_arr, axis = (0,1)) * 255, dtype = np.uint8)
    return carr

def get_nearest_colour(pixel, nc):
    return np.round(pixel * (nc - 1)) / (nc - 1)
