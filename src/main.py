from PIL import Image
import sys
import floyd_steinberg_dithering

def main():
    floyd_steinberg_dithering.apply(sys.argv[1])

if __name__ == "__main__":
    main()
