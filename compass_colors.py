from PIL import Image
from PIL import ImageDraw
import datetime
import json
import sys
import copy

size = 800

image = Image.new('RGBA',(size,size),(0,0,0,255))
draw = ImageDraw.Draw(image)

black = (0, 0, 0, 0)
table = [ [0] * 4 ] * 23

def wedges(size, count, trans):
  image = Image.new('RGBA',(size,size),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  accuracy = 1000
  delta = 360 * accuracy / (count+1)
#  print delta
  beg = 0
  for i in range(0,count+1):
          #    beg = i * delta / 100
    end = (i+1) * delta / accuracy 
#    center = (beg + end) / 2
    center = beg 
    red = 0
    blue = 0
    green = 0
    if(center < 180):
      red = 255 * (90 - abs(90 - center))/90
    if(center > 180):
      blue = 255 * (90 - abs(270 - center))/90
    if(center >= 90 and center < 270):
      green = 255 * (90 - abs(180 - center))/90
    else:
      if center < 90:
        green = 255 * (90 - center)/90
        blue = 255 * (90 - center)/90
        red = 255
      else:
        green = 255 * abs(270 - center)/90
        red = 255 * abs(270 - center)/90
        blue = 255
    color = (red, green, blue, trans)
    print color
    draw.pieslice((0,0,size, size), beg, end, color, color)
    beg = end
  return image.rotate(delta/accuracy/2)

#print json.dumps(table)
tmp = wedges(size, 31, 255)
image.paste(tmp, (0,0,size,size), tmp)

image.rotate(90).show()
