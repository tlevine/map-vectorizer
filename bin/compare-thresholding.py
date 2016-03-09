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
    if verbose:
        print('$ ' + ' '.join(command))
    stdout=p.stdout.read()
    stderr=p.stderr.read()
    if b'Error' in stdout or b'Error' in stderr or p.returncode:
        print((stderr + b'\n\n' + stdout).decode('utf-8'))
        exit(1)

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

def compare_thresholding(output_dir, input_file='test.tif'):
    '''
    Run like so.
    
        ./bin/compare-thresholding.py ~/thresholding

    Then check the contents of ~/thresholding to see what the
    thresholds look like.

        cd ~/thresholding && ls|sort -n|xargs feh

    '''
    os.makedirs(output_dir, exist_ok=True)

    brightness = range(-127, 128, 8)
    contrast = range(0, 100, 5)
    thresholdblack = range(0, 255, 8)
    thresholdwhite = range(0, 255, 8)

    p = product(thresholdwhite, thresholdblack, brightness, contrast)
    for args in p:
        fn = os.path.join(output_dir, '%d_%d_%d_%d.tif' % args)
        if not os.path.exists(fn):
            gimp_one(input_file, fn, *args)

if __name__ == '__main__':
    import horetu
    horetu.horetu(compare_thresholding)
