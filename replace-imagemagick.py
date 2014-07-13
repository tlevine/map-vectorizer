import subprocess, re, logging

def old_color(image):
    pixelvalue subprocess.Popen(["convert", "-quiet", image, "-resize", "1x1","txt:-"], stdout=subprocess.PIPE).communicate()[0]
    pattern = re.compile(r"0,0: \(([\s0-9]*),([\s0-9]*),([\s0-9]*).*")
    values = pattern.findall(pixelvalue)
    if len(values) > 0:
        red = int(values[0][0])
        green = int(values[0][1])
        blue = int(values[0][2])
        return red, green, blue

def new_color(image):


'dsv-truck.jpg'
