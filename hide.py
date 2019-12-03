from PIL import Image
import argparse

input_file = ""
output_file = ""
def hide(input_image, output_image):
        i = 0
        ch = 3 # default to RGB channels
        data = input("Please enter the data you wish to encode in the image: ")
        payload = "SteG"
        data_len = len(data)
        data_len_padded = format(len(data), '016b')
        payload_bin = bin(int.from_bytes('SteG'.encode(), 'big'))[2:]
        #payload_bin += data_len_padded
        payload_bin += format(len(bin(int.from_bytes(data.encode(), 'big'))[2:]), '016b')
        payload_bin += bin(int.from_bytes(data.encode(), 'big'))[2:]

        with Image.open(input_image) as img:
                ch = len(img.getbands())
                print("Image dimensions:", ch)
                w, h = img.size
                max_size = w * h * ch / 8 - 10 # account for misc info
                if len(data) > max_size:
                        print("Data size is greater than the image's capacity!")
                        return
                for x in range(0, w):
                        for y in range(0, h):
                                px = list(img.getpixel((x, y)))
                                for n in range(0, ch):
                                        if (i < len(payload_bin)):
                                                px[n] = px[n] & ~1  # clear existing LSB
                                                px[n] = px[n] | int(payload_bin[i])
                                                i += 1
                                img.putpixel((x,y), tuple(px))
                img.save(output_image, "PNG")
        print("Done!")

parser = argparse.ArgumentParser(description="SteG image steganography by Coppertint, data encoding")
parser.add_argument("input_image", help="Path to input image")
parser.add_argument("output_image", help="Path to output image")
args = parser.parse_args()

if __name__ == "__main__":
    hide(args.input_image, args.output_image)
