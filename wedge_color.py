from PIL import Image
from PIL import ImageDraw
import datetime
import json
import sys

size = 400

image = Image.new('RGBA',(size,size),(0,0,0,255))
draw = ImageDraw.Draw(image)

black = (0, 0, 0, 0)

def get_white_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  first = (scope[1] - scope[0] ) / 4
  third = 3 * (scope[1] - scope[0] ) / 4
  red = 0
  blue = 0
  green = 0
  if(center < half):
    red = 255 * (first - abs(first - center))/first
  if(center > half):
    blue = 255 * (first - abs(third - center))/first
  if(center >= first and center < third):
    green = 255 * (first - abs(half - center))/first
  else:
    if center < first:
      green = 255 * (first - center)/first
      blue = 255 * (first - center)/first
      red = 255
    else:
      green = 255 * abs(third - center)/first
      red = 255 * abs(third - center)/first
      blue = 255
  return (red, green, blue, 255)

def get_black_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  first = (scope[1] - scope[0] ) / 4
  third = 3 * (scope[1] - scope[0] ) / 4
  if(center < half):
    red = 255 * (first - abs(first - center))/first
  else:
    red = 0
  if(center > first and center <= third):
    green = 255 * (first - abs(half - center))/first
  else:
    green = 0
  if(center < half):
    blue = 0
  else:
    blue = 255 * (first - abs(third - center))/first
  color = (red, green, blue, 255)
  return color

def get_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  if center > half:
    return get_white_color(center, scope)
  return get_black_color(center, scope)

def wedges(count):
  accuracy = 1000
  delta = 360 * accuracy / (count+1)
  print delta
  beg = 0
  for i in range(0,count+1):
          #    beg = i * delta / 100
    end = (i+1) * delta / accuracy 
    #color = get_color(beg, (0, 360), count+1)
    color = get_color(beg, (0, 360))
    draw.pieslice((0,0,size, size), beg, end, color, color)
    beg = end
  return

wedges(127)

image.rotate(90).show()
