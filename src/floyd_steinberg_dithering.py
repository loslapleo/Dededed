from PIL import Image
import numpy as np
import progress_bar

def apply(image_name:str, nc = 8):
    image_arr = np.array(Image.open(image_name), dtype = float) / 255
    new_image = Image.fromarray(floyd_steinberg_dithering(image_arr, nc))
    new_image.save("out/fs_dither_nc{}.png".format(nc))

def floyd_steinberg_dithering(image_arr, nc):
    y_max = np.size(image_arr, axis = 0)
    x_max = np.size(image_arr, axis = 1)
    for y in range(1, y_max - 1):
        for x in range(1, x_max - 1):
            old_color = image_arr[y][x].copy()
            image_arr[y][x] = get_nearest_color(image_arr[y][x], nc)
            quant_error = old_color - image_arr[y][x]
            image_arr[y][x + 1] += quant_error * 7 / 16
            image_arr[y + 1][x - 1] += quant_error * 3 / 16
            image_arr[y + 1][x] += quant_error * 5 / 16
            image_arr[y + 1][x + 1] += quant_error / 16
        progress_bar.print_progress_bar(y, y_max, prefix = "Floyd-Steinberg", \
                length = 64)
    progress_bar.print_progress_bar(1, 1, prefix = "Floyd-Steinberg", length = 64)
    carr = np.array(image_arr / np.max(image_arr, axis = (0, 1)) * 255, dtype = np.uint8)
    return carr

def get_nearest_color(pixel, nc):
    return np.round(pixel * (nc - 1)) / (nc - 1)
