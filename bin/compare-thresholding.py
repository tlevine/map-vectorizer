#!/usr/bin/env python3
import subprocess, os, re
from itertools import product

from PIL import Image, ImageChops

def gimp_one(inputfile:'file', thresholdfile:'file',
             brightness, contrast, thresholdblack, thresholdwhite,
             gimp_path='gimp', verbose=False):
    args = {
        'inputfile': inputfile,
        'thresholdfile': thresholdfile,
        'brightness': brightness,
        'contrast': contrast,
        'thresholdblack': thresholdblack,
        'thresholdwhite': thresholdwhite,
    }
    command = [gimp_path, '-i', '-b', '-']
    p = subprocess.Popen(command, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if verbose:
        print((gimp_func % args))
    p.stdin.write((gimp_func % args).encode('utf-8'))
    p.stdin.write(b'(gimp-quit 0)\n')
    p.stdin.close()
    p.wait()
    if verbose or p.returncode:
        print('$ ' + ' '.join(command))
    if verbose:
        print(p.stdout.read())
    if p.returncode:
        print(p.stderr.read())

def compare(left, right):
    diff = ImageChops.difference(a, b)
    diff = diff.convert('L')
    diff = diff.point(point_table)
    new = diff.convert('RGB')
    new.paste(b, mask=diff)
    return new


gimp_func = '''
(let*
  (
    (image 
      (car
        (file-tiff-load RUN-NONINTERACTIVE "%(inputfile)s" "%(inputfile)s") )) 
    (drawable 
      (car 
        (gimp-image-get-layer-by-name image "Background")))) 
  (gimp-selection-none image) 
  (gimp-brightness-contrast drawable %(brightness)d %(contrast)d)
  (gimp-threshold drawable %(thresholdblack)d %(thresholdwhite)d) 
  (gimp-file-save RUN-NONINTERACTIVE image drawable "%(thresholdfile)s" "%(thresholdfile)s")
  (gimp-image-delete image))
'''


def compare(left, right):
    diff = ImageChops.difference(Image.open(left), Image.open(right))
    return sum(diff.histogram())

def gimp_many():
    brightness = range(-127, 128, 16)
    contrast = range(0, 100, 10)
    thresholdblack = range(0, 255, 16)
    thresholdwhite = range(0, 255, 16)

    for args in product(brightness, contrast, thresholdblack, thresholdwhite):
        fn = '/tmp/gimp_%d_%d_%d_%d.tif' % args
        if not os.path.isfile(fn):
            gimp_one('test.tif', fn, *args)

if __name__ == '__main__':
    gimp_many() # main()
