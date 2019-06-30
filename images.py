#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from os import path, mkdir, listdir
from threading import Thread
from PIL import Image, ImageDraw, ImageFont


"""
    Draw text on image based on the image name, resize and convert to black and white.

    Example:
    image name: author-name.jpg;
    text: © Author Name

    Default input folder with images: ./source-images/

    Default output folder for images: ./output-images/
"""


def image(in_folder: str, out_folder: str, file: str) -> None:
    """
        :param in_folder: Input folder with images.

        :param out_folder: Output folder for image.

        :param file: Image file without path.
    """
    if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
        # Get image name
        name, _ = path.splitext(file)
        text = '© ' + name.replace('-', ' ').title()

        # Open image
        img = Image.open(path.join(in_folder, file))
        # Change size
        img.thumbnail((600, 600))

        draw = ImageDraw.Draw(img)

        # Set font
        fonts_path = path.join('.', 'fonts')
        font = ImageFont.truetype(
            path.join(fonts_path, 'Microsoft Sans Serif.ttf'), size=18, encoding='utf-8')

        # Calculate text position
        img_width, img_height = img.size
        font_width, font_height = font.getsize(text)
        text_pos = (img_width-font_width-20, img_height-font_height-20)

        # Draw text, convert to black and white and save image
        draw.text(text_pos, text, (255, 255, 255), font=font)
        img.convert(mode='L').save(path.join(out_folder, name + '.png'))


def process_images(in_folder="source-images", out_folder='output-images') -> None:
    """
        :param in_folder: Input folder with images (default = './source-images').

        :param out_folder: Output folder for images (default = './output-images').
    """
    # Check input folder
    if path.exists(in_folder) is False:
        return

    #  Create directory for output images
    if path.exists(out_folder) is False:
        mkdir(out_folder)

    # Process all images in the folder
    for file in listdir(in_folder):
        thread = Thread(target=image, args=(in_folder, out_folder, file))
        thread.start()


if __name__ == "__main__":
    # Get arguments from command line
    parser = ArgumentParser()
    # Output folder for images
    parser.add_argument('--f', help='output folder name')

    args = parser.parse_args()

    if args.i is not None and args.o is None:
        process_images(in_folder=args.i)
    elif args.i is None and args.o is not None:
        process_images(out_folder=args.o)
    else:
        process_images("source-images" if args.i is None else args.i,
                       "output-images" if args.o is None else args.o)
