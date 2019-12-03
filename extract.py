#!/usr/bin/env python3
from PIL import Image
import argparse
input_file = ""

def extract(input_image):
    magic = ""
    length = ""
    i = 0
    ch = 3
    data = ""
    with Image.open(input_image) as img:
        ch = len(img.getbands())
        # print(ch)
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                for n in range(0, ch):
                    if i < 31:
                        magic += str(pixel[n] & 1)
                        i += 1
                    elif magic != "1010011011101000110010101000111":
                        print("Not a SteG file!")
                        return
                    elif i < 47:
                        length += str(pixel[n] & 1)
                        i += 1
                    elif i >= 47 and i < 47 + int(length, 2):
                        data += str(pixel[n] & 1)
                        i += 1
                    elif i >= 47 + int(length, 2):
                        #print(magic, length, i, int(length, 2), data)
                        print(int(data, 2).to_bytes((int(data, 2).bit_length() + 7) // 8, "big").decode())
                        return


parser = argparse.ArgumentParser(description="SteG image steganography by Coppertint, data extraction")
parser.add_argument("input_image", help="Path to input image")
args = parser.parse_args()

if __name__ == "__main__":
    extract(args.input_image)

