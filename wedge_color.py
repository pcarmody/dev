from PIL import Image
from PIL import ImageDraw
import datetime
import json
import sys

size = 400

image = Image.new('RGBA',(size,size),(0,0,0,255))
draw = ImageDraw.Draw(image)

black = (0, 0, 0, 0)

def wedges(count):
  accuracy = 1000
  delta = 360 * accuracy / (count+1)
  print delta
  beg = 0
  for i in range(0,count+1):
          #    beg = i * delta / 100
    end = (i+1) * delta / accuracy 
#    center = (beg + end) / 2
    center = beg 
    if(center < 180):
      red = 255 * (90 - abs(90 - center))/90
    else:
      red = 0
    if(center > 90 and center < 270):
      green = 255 * (90 - abs(180 - center))/90
    else:
      green = 0
    if(center < 179):
      blue = 0
    else:
      blue = 255 * (90 - abs(270 - center))/90
    color = (red, green, blue, 255)
    print i
    print beg
    print color
    draw.pieslice((0,0,size, size), beg, end, color, color)
    beg = end
  return

wedges(15)

image.rotate(90).show()
