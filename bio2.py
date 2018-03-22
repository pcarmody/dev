from PIL import Image
from PIL import ImageDraw
import datetime
import json

window_size = 400

image = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
draw = ImageDraw.Draw(image)

def ring_size(level):
  percentage = window_size * 10/100
  return window_size - (level * percentage)

def ring_disp(level):
  percentage = window_size * 5/100
  return level * percentage

def ring_shape(level):
  disp = ring_disp(level)
  size = ring_size(level)
  retval = (disp, disp, size+disp, size+disp)
  return retval

moon_space = ring_size(0)
moon_disp = ring_disp(0)
sun_space = ring_size(1)
sun_disp = ring_disp(1)
tide_space = ring_size(2) 
tide_disp = ring_disp(2)

def draw_halves(size, rise_angle, set_angle, day_color, night_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
#  rise_angle = 360 * moon_rise / min_per_day
#  set_angle = 360 * moon_set / min_per_day
  black = (255, 255, 255, 0)
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, black)
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, black)
  return image

#
# construct today's image
#

ring_number = 0

repeat = 53

today = datetime.date.today()
birthday = datetime.date(1962, 11, 14)
days_alive = today - birthday

def draw_circle(level, repeat, day_color, night_color):
  first_mod = days_alive.days % repeat
  half_repeat = repeat / 2
  if(first_mod / half_repeat > 0):
      mod = first_mod % half_repeat
  else:
      mod = -1 * first_mod % half_repeat
  degrees = mod * 360 / half_repeat
  
  if(degrees < 0):
    moon = draw_halves(ring_size(level), degrees, 0, day_color, night_color)
  else:   
    moon = draw_halves(ring_size(level), 0, degrees, day_color, night_color)

  return moon

day_color = (255,255,255,255)
night_color = (255,255,255,127)
moon = draw_circle(0, 23, day_color, night_color)
image.paste(moon, ring_shape(0), moon)

day_color = (255,0,0,255)
night_color = (255,0,0,127)
nest = draw_circle(1, 28, day_color, night_color)
image.paste(nest, ring_shape(1), nest)

day_color = (0, 255,0,255)
night_color = (0,255,0,127)
nest = draw_circle(2, 33, day_color, night_color)
image.paste(nest, ring_shape(2), nest)

# rotate the entire image based on the current time.
image.rotate(90).show()
