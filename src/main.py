from PIL import Image
import ordered_dithering

def main():
    try:
        ordered_dithering.apply_ordered_dithering("data/cloudy.png", 16)
    except IOError:
        pass

if __name__ == "__main__":
    main()
