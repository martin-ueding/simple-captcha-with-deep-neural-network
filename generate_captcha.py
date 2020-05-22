#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2020 Martin Ueding <dev@martin-ueding.de>

import argparse
import random

from PIL import Image, ImageFont, ImageDraw


def make_captcha():
    image = Image.new('L', (310, 80), 221)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeSans.ttf', 27)
    d = ImageDraw.Draw(image)

    d.line([0, 0, 309, 0], width=1)     # Top
    d.line([0, 79, 309, 79], width=1)   # Bottom
    d.line([309, 0, 309, 79], width=1)  # Right
    d.line([0, 0, 0, 79], width=1)      # Left

    for i in range(15):
        ellipse_width = 16
        ellipse_height = 8
        bbox = (image.width // 2 - i * ellipse_width,
                image.height // 2 - i * ellipse_height,
                image.width // 2 + i * ellipse_width,
                image.height // 2 + i * ellipse_height)
        d.ellipse(bbox, outline=0)

    allowed_digits = [2, 3, 4, 5, 6, 8]
    digits = []
    for x in [17, 57, 115, 170, 217, 260]:
        txt = Image.new('LA', (20, 25), (150, 0))
        dx = ImageDraw.Draw(txt)
        digit = random.choice(allowed_digits)
        digits.append(digit)
        dx.text((0, 0), str(digit), font=font, fill=(0, 255))
        w = txt.rotate(random.uniform(-45, 45), expand=1)
        y = random.randint(14, 45)
        image.paste(w, (x, y), w.getchannel('A'))

    for i in range(500):
        x = random.randint(0, 309)
        y = random.randint(0, 79)
        image.putpixel((x, y), 0)

    filename = '{}-{}.png'.format(
        ''.join(map(str, digits)),
        random.randint(1000, 9999))

    image.save(filename)


def main():
    options = _parse_args()

    for i in range(options.count):
        make_captcha()



def _parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('count', type=int, default=1)
    options = parser.parse_args()

    return options


if __name__ == '__main__':
    main()
