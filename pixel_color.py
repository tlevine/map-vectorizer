'''
The two methods produce different colors, but they're both bluish.
Figure out what resizing algorithm convert uses, and you can probably
produce the same thing with PIL/pillow.
'''
import subprocess, re, logging

from PIL import Image

def old_color(image):
    pixelvalue = subprocess.Popen(["convert", "-quiet", image, "-resize", "1x1","txt:-"], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    pattern = re.compile(r"0,0: \(([\s0-9]*),([\s0-9]*),([\s0-9]*).*")
    values = pattern.findall(pixelvalue)
    if len(values) > 0:
        red = int(values[0][0])
        green = int(values[0][1])
        blue = int(values[0][2])
        return red, green, blue

def new_color(image):
    return Image.open(image).resize((1,1)).getpixel((0,0))
