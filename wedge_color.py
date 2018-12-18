from PIL import Image
from PIL import ImageDraw
import datetime
import json
import sys

size = 400

image = Image.new('RGBA',(size,size),(0,0,0,255))
draw = ImageDraw.Draw(image)

black = (0, 0, 0, 0)

color_list = (
    (0, 0, 0, 255),
    (255, 0, 0, 255),
    (255, 255, 0, 255),
    (0, 255, 0, 255),
    (0, 0, 255, 255),           #4b0082
    (75, 0, 130, 255),          #4b0082
    (238, 130, 238, 255),       # ee82ee
    (255, 255, 255, 255),
    (0, 0, 0, 255),
)
color_count = 7
#color_list = (
#    (0, 0, 255, 255),   # Bright Blue,
#    (255, 255, 255, 255), # Black,
#    (0, 0, 0, 255),     # White,
#    (0, 0, 0, 255),
#)
#color_count = 2

def map_color_value(value, scope):
        
  delta = scope / color_count           # how wide the wedge of color is
  left = value / delta                  # the color of the wedge
#  right = (left + 1) % color_count      # the next color
  right = (left + 1)                     # the next color
  mod = value % delta                   # how deep into the wedge of color
  
  right_weight = mod * 100 / delta      
  left_weight = (delta - mod) * 100 / delta

  ret_val= []

  for i in range(0,4):
    ret_val.append( ( color_list[left][i] * left_weight + color_list[right][i] * right_weight) / 100 )

  return ( ret_val[0], ret_val[1], ret_val[2], ret_val[3])

def get_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  return map_color_value(center, 360)

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
    tmp = 0
    for i in range(0,3):
      tmp = tmp * 256 + color[i]
    print " "+str(i)+":"+str(color)+":"+str(color[0])+":"+str(color[1])+":"+str(color[2])
    draw.pieslice((0,0,size, size), beg, end, color, color)
    beg = end
  return

wedges(23)

image.rotate(90).show()
